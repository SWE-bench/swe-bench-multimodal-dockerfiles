import json
import re
from argparse import ArgumentParser
from pathlib import Path

from .constants import (
    CONTAINER_WORKDIR,
    PINNED_CHROME_VERSION,
    END_TEST_OUTPUT,
    INSTANCE_OVERRIDES,
    MAP_REPO_VERSION_TO_SPECS_JS,
    START_TEST_OUTPUT,
)
from .assets import PROBLEM_ASSETS_DIR
from .utils import (
    git_clone_timesafe,
    make_heredoc_run_command,
)


_DOCKERFILE_BASE_JS = r"""
FROM --platform=linux/amd64 ubuntu:jammy

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Etc/UTC

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libssl-dev \
    software-properties-common \
    wget \
    gnupg \
    jq \
    ca-certificates \
    dbus \
    ffmpeg \
    imagemagick \
    unzip \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update \
    && apt-get install -y fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
        fonts-khmeros fonts-kacst fonts-freefont-ttf libxss1 dbus dbus-x11 \
        --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
# Pin Chrome. The apt repo only ever serves the current stable, so an unpinned install
# silently changes version on every rebuild -- Chrome 151 broke openlayers' WebGL and
# Cypress's browser connection that way. Chrome for Testing archives every build, so this
# stays reproducible. Keep both binary names: 160 eval scripts reference one or the other.
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/__CHROME_VERSION__/linux64/chrome-linux64.zip -O /tmp/chrome.zip \
    && unzip -q /tmp/chrome.zip -d /opt/chrome-pinned \
    && rm /tmp/chrome.zip \
    && printf '#!/bin/bash\nexec /opt/chrome-pinned/chrome-linux64/chrome "$@"\n' > /usr/bin/google-chrome \
    && chmod +x /usr/bin/google-chrome \
    && cp /usr/bin/google-chrome /usr/bin/google-chrome-stable

ENV NVM_DIR /usr/local/nvm

RUN mkdir -p $NVM_DIR
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.3/install.sh | bash
RUN apt-get update && apt-get install -y \
    procps \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdrm2 \
    libgbm1 libgconf-2-4 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 \
    libnss3 libpango-1.0-0 libpangocairo-1.0-0 libxcomposite1 \
    libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 libxss1 libxshmfence1 libglu1 \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN /usr/bin/google-chrome
RUN echo "CHROME_BIN=$CHROME_BIN" >> /etc/environment
RUN mkdir -p /run/dbus

ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/run/dbus/system_bus_socket"

RUN dbus-daemon --system --fork

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
# puppeteer v20+ renamed the variable; without it install.mjs hangs fetching Chrome
ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV OPENSSL_CONF /etc/ssl

RUN useradd -m chromeuser

USER chromeuser

WORKDIR /home/chromeuser

USER root
"""


# ── Dockerfile generation ──────────────────────────────────────────────


def make_env_script_list(instance, specs):
    docker_specs = {
        **specs.get("docker_specs", {}),
        **INSTANCE_OVERRIDES.get(instance["instance_id"], {}).get("docker_specs", {}),
    }
    node_version = docker_specs.get("node_version", "18.17.1")
    pnpm_version = docker_specs.get("pnpm_version", None)
    python_version = docker_specs.get("python_version", "3.9")
    commands = []
    if "apt-pkgs" in specs:
        apt_packages = " ".join(specs["apt-pkgs"])
        commands.extend([
            "apt-get update",
            f"apt-get install -y {apt_packages}",
            "rm -rf /var/lib/apt/lists/*",
        ])
    commands.extend([
        f"export NODE_VERSION={node_version}",
        "source $NVM_DIR/nvm.sh",
        "nvm install $NODE_VERSION",
        "nvm alias default $NODE_VERSION",
        "nvm use default",
    ])
    commands.extend([
        "add-apt-repository ppa:deadsnakes/ppa",
        "apt-get update",
        f"apt-get install -y python{python_version}",
        f"ln -sf /usr/bin/python{python_version} /usr/bin/python",
    ])
    commands.append("apt-get install -y python2")
    commands.extend([
        f'echo "export NODE_PATH=$NVM_DIR/v{node_version}/lib/node_modules" >> /etc/environment',
        f'echo "export PATH=$NVM_DIR/versions/node/v{node_version}/bin:$PATH" >> /etc/environment',
    ])
    if pnpm_version:
        commands.extend([
            f"export PNPM_VERSION={pnpm_version}",
            "export PNPM_HOME=/usr/local/pnpm",
            "mkdir -p $PNPM_HOME",
            'wget -qO $PNPM_HOME/pnpm "https://github.com/pnpm/pnpm/releases/download/v$PNPM_VERSION/pnpm-linux-x64"',
            "chmod +x $PNPM_HOME/pnpm",
            "ln -s $PNPM_HOME/pnpm /usr/local/bin/pnpm",
            'echo "export PNPM_HOME=$PNPM_HOME" >> /etc/profile',
            'echo "export PATH=$PNPM_HOME:$PATH" >> /etc/profile',
        ])
    commands.extend([
        "source $NVM_DIR/nvm.sh && node -v",
        "source $NVM_DIR/nvm.sh && npm -v",
        "python -V",
        "python2 -V",
    ])
    if pnpm_version:
        commands.append("pnpm -v")
    return make_heredoc_run_command(commands)


def make_repo_script_list(specs, repo, base_commit, instance_id=None):
    commands = [
        *git_clone_timesafe(repo, base_commit, CONTAINER_WORKDIR),
        f"cd {CONTAINER_WORKDIR}",
        "git clean -fdxq",
    ]
    commands.append("source $NVM_DIR/nvm.sh")
    commands.extend(INSTANCE_OVERRIDES.get(instance_id, {}).get("install_pre", []))
    override_install = INSTANCE_OVERRIDES.get(instance_id, {}).get("install")
    if override_install:
        commands.extend(override_install)
    elif "install" in specs:
        install_commands = specs["install"]
        if isinstance(install_commands, str):
            install_commands = [install_commands]
        commands.extend(install_commands)
    if "build" in specs:
        build_commands = specs["build"]
        if isinstance(build_commands, str):
            build_commands = [build_commands]
        commands.extend(build_commands)
    commands.extend(INSTANCE_OVERRIDES.get(instance_id, {}).get("install_post", []))
    # install/build run as root and leave root-owned artifacts (e.g. openlayers' build/),
    # but the eval script runs the tests as chromeuser. chmod again at the very end so
    # those directories stay writable.
    commands.append(f"chmod -R 777 {CONTAINER_WORKDIR}")
    return make_heredoc_run_command(commands)


def _strip_binary_diffs(patch_text: str) -> tuple[str, list[str]]:
    """Strip binary file diffs from a patch, returning cleaned patch and list of binary file paths.

    Binary diffs (containing 'Binary files ... differ') can't be applied by git apply
    when the patch was generated without --binary. We strip them and handle the binary
    files separately via image_assets downloads.
    """
    lines = patch_text.split("\n")
    cleaned = []
    binary_files = []
    skip_until_next_diff = False

    for i, line in enumerate(lines):
        if line.startswith("diff --git "):
            skip_until_next_diff = False
            # Look ahead for Binary marker
            for j in range(i + 1, min(len(lines), i + 6)):
                if "Binary files" in lines[j] and "differ" in lines[j]:
                    skip_until_next_diff = True
                    match = re.search(r"diff --git a/.* b/(.*)", line)
                    if match:
                        binary_files.append(match.group(1))
                    break
                if lines[j].startswith("diff --git "):
                    break
        if not skip_until_next_diff:
            cleaned.append(line)

    return "\n".join(cleaned), binary_files


def _make_image_download_script(instance: dict, task_dir=None) -> str:
    """Generate a RUN block to download image_assets into staging dirs at build time."""
    image_assets = instance.get("image_assets")
    if not image_assets:
        return ""
    if isinstance(image_assets, str):
        image_assets = json.loads(image_assets) if image_assets else {}

    commands = ["mkdir -p /swebench/image_assets"]

    # test_patch images → /swebench/image_assets/test_patch/{repo_relative_path}
    test_patch_assets = image_assets.get("test_patch", [])
    if hasattr(test_patch_assets, "tolist"):
        test_patch_assets = test_patch_assets.tolist()
    for item in test_patch_assets:
        if isinstance(item, str):
            item = json.loads(item)
        path = item.get("path", "")
        url = item.get("url", "")
        if path and url:
            dest = f"/swebench/image_assets/test_patch/{path}"
            commands.append(f"mkdir -p $(dirname '{dest}')")
            commands.append(f"curl -fsSL -o '{dest}' '{url}' || true")

    # problem_statement images land in /problem_assets via COPY. Only the handful
    # with no archived copy are still fetched, into the same directory under the
    # archive's own name, so everything a statement links to sits in one place.
    for name, url in _unarchived_problem_images(instance, task_dir):
        dest = f"/problem_assets/{name}"
        commands.append("mkdir -p /problem_assets")
        commands.append(f"curl -fsSL -o '{dest}' '{url}' || true")

    if len(commands) <= 1:
        return ""
    return make_heredoc_run_command(commands)


def _problem_images(instance: dict, task_dir=None):
    """Every problem-statement image, as (archive filename, url, is archived)."""
    if task_dir is None:
        return []
    from .assets import _problem_image_targets

    return [
        (path.name, url, path.is_file())
        for path, url in _problem_image_targets(task_dir, instance)
    ]


def _unarchived_problem_images(instance: dict, task_dir=None) -> list[tuple[str, str]]:
    """The ones with no local copy, deduplicated by url as the download was."""
    out, seen = [], set()
    for name, url, archived in _problem_images(instance, task_dir):
        if archived or url in seen:
            continue
        seen.add(url)
        out.append((name, url))
    return out


def _make_problem_asset_copies(instance: dict, task_dir=None) -> str:
    """COPY the task's archived assets to /problem_assets in the image.

    The whole directory, under the names it is archived with: the index prefix keeps
    images distinct where two of them share a filename, and a statement that links a
    reproduction as well as a screenshot gets both.
    """
    if task_dir is None or not (task_dir / PROBLEM_ASSETS_DIR).is_dir():
        return ""
    return f'COPY ["{PROBLEM_ASSETS_DIR}", "/{PROBLEM_ASSETS_DIR}"]'


def _get_dockerfile(instance, task_dir=None) -> str:
    repo = instance["repo"]
    version = instance.get("version") or None
    base_commit = instance["base_commit"]
    specs = MAP_REPO_VERSION_TO_SPECS_JS[repo][version]
    dockerfile = _DOCKERFILE_BASE_JS.replace("__CHROME_VERSION__", PINNED_CHROME_VERSION)
    # per-instance docker_specs win over the repo/version spec, so one instance can move
    # off a shared node version without disturbing its siblings
    docker_specs = {
        **specs.get("docker_specs", {}),
        **INSTANCE_OVERRIDES.get(instance["instance_id"], {}).get("docker_specs", {}),
    }
    node_version = docker_specs.get("node_version", "18.17.1")
    pnpm_version = docker_specs.get("pnpm_version", None)
    dockerfile += f"\nENV NODE_VERSION {node_version}\n"
    dockerfile += "ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules\n"
    dockerfile += "ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH\n"
    if pnpm_version:
        dockerfile += f"ENV PNPM_VERSION {pnpm_version}\n"
        dockerfile += "ENV PNPM_HOME /usr/local/pnpm\n"
        dockerfile += "ENV PATH $PNPM_HOME:$PATH\n"
    env_script = make_env_script_list(instance, specs)
    if env_script:
        dockerfile += f"\n{env_script}\n"
    repo_script = make_repo_script_list(specs, repo, base_commit, instance["instance_id"])
    if repo_script:
        dockerfile += f"\n{repo_script}\n"
    # Download image_assets at build time
    image_script = _make_image_download_script(instance, task_dir)
    if image_script:
        dockerfile += f"\n{image_script}\n"
    copies = _make_problem_asset_copies(instance, task_dir)
    if copies:
        dockerfile += f"\n{copies}\n"
    dockerfile += f"\nWORKDIR {CONTAINER_WORKDIR}\n"
    return dockerfile


# ── Per-instance test command generators ──────────────────────────────
# Ported from SWE-bench/private test_spec/javascript.py.
# JS test frameworks often need specific test paths/patterns rather than
# running the entire suite.

try:
    from unidiff import PatchSet
except ImportError:
    PatchSet = None


def _get_test_paths(instance: dict) -> list[str]:
    """Extract test file paths from test_patch."""
    test_patch = instance.get("test_patch", "")
    if not test_patch:
        return []
    if PatchSet is not None:
        return [x.path for x in PatchSet(test_patch)]
    return re.findall(r"diff --git a/.* b/(.*)", test_patch)


def _get_test_cmds_prism(instance: dict) -> list:
    test_cmd = MAP_REPO_VERSION_TO_SPECS_JS[instance["repo"]][instance.get("version") or None]["test_cmd"]
    directives = []
    for test_path in _get_test_paths(instance):
        if test_path.startswith("tests/languages"):
            directives.append(test_cmd + f" --language {test_path.split('/')[2]}")
        elif test_path == "tests/core/greedy.js":
            directives.append("./node_modules/.bin/mocha tests/core/**/*.js --reporter json")
        elif test_path == "test.html":
            continue
    return sorted(list(set(directives)))


def _get_test_cmds_openlayers(instance: dict) -> list:
    SET_PUPPETEER = "PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable"
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    SSL_LEGACY = "NODE_OPTIONS=--openssl-legacy-provider"
    cmds = []
    for test_path in _get_test_paths(instance):
        test_type = test_path.split('/')[1] if '/' in test_path else ""
        if test_type == "browser":
            if instance.get("version") in ['6.9', '6.12', '6.14', '7.0', '7.1', '7.2', '7.3', '7.5']:
                cmds.append(f'su chromeuser -c "npm run test-browser"')
            else:
                cmds.append(f'{SET_PUPPETEER} {XVFB} su chromeuser -c "npm run test-browser"')
        elif test_type == "rendering":
            # v7.4: use Puppeteer's bundled Chromium 115 via Xvfb (not --headless,
            # which uses SwiftShader and hangs in Docker). --force continues past failures.
            if instance.get("version") in ['7.4']:
                PENV = "CI=true PUPPETEER_CACHE_DIR=/home/chromeuser/.cache/puppeteer"
                cmds.append(
                    f'{PENV} {XVFB} su chromeuser -c "'
                    f'{PENV} npm run build-full && {PENV} '
                    f'node test/rendering/test.js --force --headless --log-level info"'
                )
            else:
                # CI=1 makes puppeteer headless with --no-sandbox, which is the config
                # upstream used to generate the expected.png baselines; without it
                # rendering is ~97% off. --no-sandbox also removes the need for an
                # unprivileged user, and running as root lets the harness write
                # actual.png into the root-owned /testbed. --log-level info surfaces
                # passing cases ("<case>': ok"), the only positive evidence that an
                # all-passing run actually executed, since the parser records only
                # failures.
                # --headless explicitly: CI=1 only implies headless on the newer
                # harness; v5.x hardcodes `headless: false` and CI-gates just the
                # sandbox args, leaving rendering ~98% off under Xvfb.
                cmds.append(
                    f'CI=1 {SET_PUPPETEER} {XVFB} '
                    f'npm run test-rendering -- --headless --log-level info'
                )
        elif test_type == "spec":
            cmds.append(f'{SET_PUPPETEER} {XVFB} su chromeuser -c "npm run karma -- --single-run --log-level error"')
        elif test_type == "node":
            cmds.append("npm run test-node")
        else:
            cmds.append("npm run test")
        if test_type in ['spec', 'rendering', 'browser'] and instance.get('version') in [
            '6.1', '6.2', '6.3', '6.4', '6.5', '6.5.1', '6.6',
            '4.3', '4.4', '4.5', '4.6', '5.1', '5.2', '5.3'
        ]:
            cmds[-1] = f"{SSL_LEGACY} {cmds[-1]}"
    return sorted(set(cmds))


def _get_test_cmds_next(instance: dict) -> list:
    SET_PUPPETEER = "PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable"
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    return sorted(set([
        # 5m cut off legitimate runs (alibaba-fusion__next-4182 died at 382s with its
        # graded tests passing). Keep this well under the harness's 1800s per-instance
        # cap minus the 900s npm install: 20m here pushed 7 instances over it.
        f'timeout 10m bash -c \'{SET_PUPPETEER} {XVFB} '
        f'su chromeuser -c "npm run test {test_path.split("/")[1]}"\''
        for test_path in _get_test_paths(instance)
    ]))


def _get_test_cmds_carbon(instance: dict) -> list:
    cmds = []
    # uncapped jest spawns a worker per core in every container; capping is both faster
    # and stops the accessibility-checker engine fetch failing under contention
    max_workers = " --maxWorkers=1" if instance.get("version") == "12" else " --maxWorkers=4"
    for test_path in _get_test_paths(instance):
        if re.search(r"__snapshots__/(.*).js.snap$", test_path):
            test_path = "/".join(test_path.split("/")[:-2])
        if "__tests__" in test_path:
            test_path = test_path.split("__tests__")[0]
        # For paths under packages/*/src/components/*/next/ or packages/cra-template/,
        # Jest won't match the specific file. Target the component directory instead.
        if "/next/" in test_path and "/components/" in test_path:
            test_path = test_path.split("/next/")[0]
        # cra-template is created by the gold patch as a standalone CRA template.
        # It needs: (1) react-router-dom installed, (2) automatic JSX transform
        # (template files don't import React), (3) bypass modulePathIgnorePatterns.
        if "cra-template/template/" in test_path:
            # cra-template is created by gold patch as a CRA template. Its deps
            # (react-router-dom, @apollo/client, etc.) are listed in template.json
            # but not in package.json. Copy them over and yarn install so PnP can
            # resolve them. Then run jest with automatic JSX runtime.
            cmds.append(
                "node -e '"
                'const p=require("./packages/cra-template/package.json");'
                'p.dependencies={"@apollo/client":"3.7.4","react-router-dom":"6.6.2",'
                '"@testing-library/react":"12.1.5","@testing-library/jest-dom":"5.16.5",'
                '"@testing-library/user-event":"12.8.3","graphql":"16.6.0",'
                '"react":"17.0.1","react-dom":"17.0.1"};'
                'require("fs").writeFileSync("packages/cra-template/package.json",JSON.stringify(p,null,2));'
                "' && yarn install 2>&1 | tail -3 ; "
                'npx jest --no-colors '
                """--config '{"preset":"jest-config-carbon","transform":{"^.+\\\\.(js|jsx)$":["babel-jest",{"presets":["@babel/preset-env",["@babel/preset-react",{"runtime":"automatic"}]]}]}}' """
                'packages/cra-template/template/src'
            )
            continue
        # e2e test files (.e2e.js) are not matched by Jest — target the component directory
        if test_path.endswith(".e2e.js"):
            test_path = "/".join(test_path.split("/")[:-1])
        cmds.append(f"yarn test{max_workers} {test_path}")
    return sorted(set(cmds))


def _get_test_cmds_scratch_gui(instance: dict) -> list:
    test_prefix = MAP_REPO_VERSION_TO_SPECS_JS[instance['repo']][instance['version']]["test_cmd"]
    cmds = []
    for test_path in _get_test_paths(instance):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        cmds.append(f"{test_prefix} {test_path}")
    return sorted(set(cmds))


def _get_test_cmds_calypso(instance: dict) -> list:
    # parse_log_calypso splits the log on " ./node_modules/.bin/jest " and reads the
    # verbose tick/cross lines, so jest has to be called directly rather than through
    # `npm run test-client`, and with --verbose or a passing suite prints no test names.
    # It also stops at the first "  ● ", so only the patched files are run: a full-suite
    # run has failing suites whose markers truncate the parse.
    cmds = []
    for test_path in _get_test_paths(instance):
        # a snapshot is checked by the test file beside it
        if "__snapshots__/" in test_path and test_path.endswith(".snap"):
            test_path = test_path.replace("__snapshots__/", "")[: -len(".snap")]
        # jest only collects client/**/test/*.js(x); mocks, fixtures and config files
        # in the same patch match nothing, and "No tests found" exits non-zero, which
        # makes the whole run ungradeable
        if not re.search(r"/test/[^/]+\.jsx?$", test_path):
            continue
        cmds.append(
            "CFG=test/client/jest.config.json; [ -f $CFG ] || CFG=test/client/jest.config.js; "
            f"./node_modules/.bin/jest --verbose -c=$CFG {test_path}"
        )
    return sorted(set(cmds))


def _get_test_cmds_lighthouse(instance: dict) -> list:
    cmds = []
    SUBDIRS = ["report", "cli", "report", "treemap", "viewer"]
    LH_PREFIX = "lighthouse-"
    for test_path in _get_test_paths(instance):
        if any(test_path.endswith(ext) for ext in [".html", ".json", ".md", ".txt"]) or "smokehouse" in test_path:
            continue
        # Skip snapshot files — target the directory instead
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0].rstrip("/")
        # Skip non-test helper files (e.g. fake-driver.js) — target the directory
        if not test_path.endswith("-test.js") and not test_path.endswith("-test.ts") and test_path.endswith(".js"):
            test_path = "/".join(test_path.split("/")[:-1])
        parent_folder = test_path.split("/")[0]
        if instance.get("version") in ['9.5', '10.0', '10.2']:
            if parent_folder == "flow-report":
                cmds.append("yarn unit-flow")
            elif parent_folder in SUBDIRS + [LH_PREFIX + x for x in SUBDIRS]:
                if parent_folder.startswith(LH_PREFIX):
                    parent_folder = parent_folder[len(LH_PREFIX):]
                cmds.append(f"yarn unit-{parent_folder} {test_path}")
            else:
                cmds.append(f"yarn mocha {test_path}")
        elif '3.0' <= str(instance.get("version", "")) <= '8.6':
            cmds.append(f"yarn jest --no-colors {test_path}")
        else:
            cmds.append(f"./node_modules/.bin/mocha --reporter json {test_path}")
    return sorted(set(cmds))


def _get_test_cmds_prettier(instance: dict) -> list:
    cmds = []
    for test_path in _get_test_paths(instance):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        if test_path.endswith(".md"):
            test_path = "/".join(test_path.split("/")[:-1])
        # Only jsfmt.spec.js and __tests__/*.js are actual specs — everything else
        # (fixture .js, .ts, .css, .snap, etc.) needs the directory instead
        if not test_path.endswith("jsfmt.spec.js") and not "/__tests__/" in test_path and not test_path.endswith("/"):
            test_path = "/".join(test_path.split("/")[:-1])
        cmds.append(f"yarn test {test_path}")
    return sorted(set(cmds))


_MAP_REPO_TO_TEST_CMDS = {
    "alibaba-fusion/next": _get_test_cmds_next,
    "Automattic/wp-calypso": _get_test_cmds_calypso,
    "carbon-design-system/carbon": _get_test_cmds_carbon,
    "GoogleChrome/lighthouse": _get_test_cmds_lighthouse,
    "openlayers/openlayers": _get_test_cmds_openlayers,
    "prettier/prettier": _get_test_cmds_prettier,
    "PrismJS/prism": _get_test_cmds_prism,
    # scratch-gui: static test_cmd runs all jest tests, works fine.
    # Per-instance cmd is too narrow (misses F2P tests not in test_patch).
    # react-pdf: static test_cmd runs the whole monorepo, which is what its
    # P2P lists need -- they span packages the patched one does not contain.
}


def _get_test_commands(instance: dict, specs: dict) -> str:
    """Get test command(s) for an instance. Uses per-repo handler if available."""
    repo = instance["repo"]
    if repo in _MAP_REPO_TO_TEST_CMDS and instance.get("test_patch"):
        cmds = _MAP_REPO_TO_TEST_CMDS[repo](instance)
        if cmds:
            # Use ; instead of && so all test commands run even if one fails.
            # We need output from ALL tests for correct F2P/P2P grading.
            return " ; ".join(cmds)
    # Fallback to static test_cmd from specs
    test_cmd = specs["test_cmd"]
    if isinstance(test_cmd, list):
        return " ; ".join(test_cmd)
    return test_cmd


# ── Eval script generation ─────────────────────────────────────────────


def _get_eval_script(instance: dict) -> str:
    """Generate the eval.sh script for a multimodal instance."""
    repo = instance["repo"]
    version = instance.get("version") or None
    base_commit = instance["base_commit"]
    test_patch = instance.get("test_patch", "")
    specs = MAP_REPO_VERSION_TO_SPECS_JS[repo][version]

    test_command = _get_test_commands(instance, specs)

    eval_commands = [
        "#!/bin/bash",
        "set -uxo pipefail",
        f"cd {CONTAINER_WORKDIR}",
        f"git config --global --add safe.directory {CONTAINER_WORKDIR}",
        "source $NVM_DIR/nvm.sh",
        "git status",
        "git show",
        f"git -c core.fileMode=false diff {base_commit}",
    ]

    # Carbon: accessibility-checker races on mkdir for engine dir when parallel workers
    # all try to download rules simultaneously. Pre-create the dir to avoid EEXIST.
    if repo == "carbon-design-system/carbon":
        eval_commands.append("mkdir -p node_modules/accessibility-checker/lib/engine 2>/dev/null || true")
    # Carbon: gold patch modifies source files — rebuild so tests use updated code.
    # The image's yarn build output is stale after the gold patch is applied.
    _CARBON_POST_PATCH_BUILD = {"16.16", "18.14"}
    if repo == "carbon-design-system/carbon" and version in _CARBON_POST_PATCH_BUILD:
        eval_commands.append("yarn build 2>&1 | tail -5 || true")

    if test_patch:
        # Strip binary diffs — they can't be applied via heredoc
        clean_test_patch, binary_files = _strip_binary_diffs(test_patch)

        test_files = re.findall(r"diff --git a/.* b/(.*)", test_patch)
        # Separate existing files (can git checkout) from new files (need rm)
        new_file_markers = set()
        lines = test_patch.split("\n")
        for i, line in enumerate(lines):
            if "new file mode" in line:
                for j in range(max(0, i - 2), i):
                    m = re.match(r"diff --git a/.* b/(.*)", lines[j])
                    if m:
                        new_file_markers.add(m.group(1))
                        break
        existing_files = [f for f in test_files if f not in new_file_markers]
        new_files = [f for f in test_files if f in new_file_markers]

        reset_parts = []
        if existing_files:
            reset_parts.append(f"git checkout {base_commit} {' '.join(existing_files)}")
        if new_files:
            reset_parts.append(f"rm -f {' '.join(new_files)}")
        reset_tests_command = " && ".join(reset_parts) if reset_parts else "true"

        eval_commands.append(reset_tests_command)

        # Apply text-only portion of test_patch
        if clean_test_patch.strip():
            HEREDOC_DELIMITER = "EOF_114329324912"
            apply_test_patch_command = (
                f"git apply -v - <<'{HEREDOC_DELIMITER}'\n{clean_test_patch}\n{HEREDOC_DELIMITER}"
            )
            eval_commands.append(apply_test_patch_command)

        # Restore binary files from build-time staging dir
        if binary_files:
            eval_commands.append(
                "test -d /swebench/image_assets/test_patch && "
                "cp -a /swebench/image_assets/test_patch/. /testbed/ 2>/dev/null || true"
            )

    # Lighthouse v1.x: gold patch may add new modules that need linking
    if repo == "GoogleChrome/lighthouse" and version and version.startswith("1."):
        eval_commands.append("npm run install-all 2>/dev/null || true")

    # Next v1.27: Cypress/Vite tests run as chromeuser; ensure writable dirs
    if repo == "alibaba-fusion/next" and version == "1.27":
        eval_commands.append("chmod -R a+w /testbed/node_modules 2>/dev/null || true")

    # OL v7.4: rendering tests need Puppeteer's bundled Chromium (115.0.5790.98)
    # for pixel-exact match with expected.png. Download directly (install.js hangs).
    # Puppeteer 20.9.0 expects: $CACHE/chrome/linux-115.0.5790.98/chrome-linux64/chrome
    if repo == "openlayers/openlayers" and version == "7.4":
        cache = "/home/chromeuser/.cache/puppeteer"
        chrome_dir = f"{cache}/chrome/linux-115.0.5790.98"
        eval_commands.extend([
            f"mkdir -p {chrome_dir}",
            f"wget -q https://storage.googleapis.com/chrome-for-testing-public/115.0.5790.98/linux64/chrome-linux64.zip -O /tmp/chrome.zip",
            f"python3 -c \"import zipfile; zipfile.ZipFile('/tmp/chrome.zip').extractall('{chrome_dir}')\"",
            "rm /tmp/chrome.zip",
            f"chmod -R 755 {chrome_dir}/chrome-linux64",
            f"chown -R chromeuser:chromeuser {cache}",
        ])

    # a patch that changes package.json leaves node_modules stale; without the skip
    # guard the reinstall blocks forever fetching Chromium
    eval_commands.append(
        'if ! git diff --quiet HEAD -- package.json 2>/dev/null; then '
        'echo "package.json changed by patch; re-syncing dependencies"; '
        "export PUPPETEER_SKIP_DOWNLOAD=true PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true; "
        "if [ -f yarn.lock ]; then timeout 900 yarn install --silent > /dev/null 2>&1 || true; "
        "else timeout 900 npm install --silent > /dev/null 2>&1 || true; fi; "
        "chmod -R a+rX node_modules > /dev/null 2>&1 || true; "
        "fi"
    )

    eval_commands += INSTANCE_OVERRIDES.get(instance["instance_id"], {}).get("eval_pre", [])

    eval_commands += [
        f": '{START_TEST_OUTPUT}'",
        test_command,
        f": '{END_TEST_OUTPUT}'",
    ]

    if test_patch:
        eval_commands.append(reset_tests_command)

    return "\n".join(eval_commands) + "\n"


# ── CLI ────────────────────────────────────────────────────────────────


def load_instances(
    dataset_name_or_path: str,
    split: str = "test",
    instance_ids: list[str] | None = None,
):
    """Load instances from HuggingFace dataset name or local JSON/JSONL file."""
    path = Path(dataset_name_or_path)
    if path.exists() and path.is_file():
        if path.suffix == ".jsonl":
            with open(path) as f:
                instances = [json.loads(line) for line in f if line.strip()]
        else:
            with open(path) as f:
                instances = json.load(f)
            if isinstance(instances, dict):
                instances = list(instances.values())
        if instance_ids:
            instance_ids_set = set(instance_ids)
            instances = [
                i for i in instances if i["instance_id"] in instance_ids_set
            ]
        return instances
    # Fall back to HuggingFace (optional dependency)
    from swebench.harness.utils import load_swebench_dataset

    return load_swebench_dataset(
        dataset_name_or_path, split, instance_ids=instance_ids
    )


def regenerate(instance_ids: list[str] | None = None) -> int:
    """Rewrite Dockerfile and eval.sh for each task, from its task.yaml."""
    from .tasks import load_task, task_dirs, write_generated

    wanted = set(instance_ids or [])
    count = 0
    for task_dir in task_dirs():
        if wanted and task_dir.name not in wanted:
            continue
        instance = load_task(task_dir)
        write_generated(
            task_dir, _get_dockerfile(instance, task_dir), _get_eval_script(instance)
        )
        count += 1
    return count


def main():
    parser = ArgumentParser(
        description="Regenerate Dockerfile and eval.sh for SWE-bench Multimodal tasks"
    )
    parser.add_argument("--instance_ids", nargs="+", default=None)
    args = parser.parse_args()
    print(f"regenerated {regenerate(args.instance_ids)} tasks")


if __name__ == "__main__":
    main()
