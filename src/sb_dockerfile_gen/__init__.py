import json
import re
from argparse import ArgumentParser
from pathlib import Path

from sb_dockerfile_gen.constants import (
    CONTAINER_WORKDIR,
    END_TEST_OUTPUT,
    MAP_REPO_VERSION_TO_SPECS_JS,
    START_TEST_OUTPUT,
)
from sb_dockerfile_gen.utils import (
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
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
        fonts-khmeros fonts-kacst fonts-freefont-ttf libxss1 dbus dbus-x11 \
        --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

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
ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV OPENSSL_CONF /etc/ssl

RUN useradd -m chromeuser

USER chromeuser

WORKDIR /home/chromeuser

USER root
"""


# ── Dockerfile generation ──────────────────────────────────────────────


def make_env_script_list(instance, specs):
    docker_specs = specs.get("docker_specs", {})
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


def make_pre_install_script(specs):
    """Generate a RUN block for pre_install commands (cached across instances).

    Commands in specs["pre_install"] run in their own Docker layer before
    git clone, so they are shared across all instances of the same repo/version.
    Use this for expensive, repo-independent installs (TinyTeX, R packages, etc.).
    """
    pre_install = specs.get("pre_install")
    if not pre_install:
        return ""
    commands = list(pre_install) if isinstance(pre_install, list) else [pre_install]
    return make_heredoc_run_command(commands)


def make_repo_script_list(specs, repo, base_commit):
    commands = [
        *git_clone_timesafe(repo, base_commit, CONTAINER_WORKDIR),
        f"cd {CONTAINER_WORKDIR}",
        "git clean -fdxq",
    ]
    commands.append("source $NVM_DIR/nvm.sh")
    if "install" in specs:
        install_commands = specs["install"]
        if isinstance(install_commands, str):
            install_commands = [install_commands]
        commands.extend(install_commands)
    if "build" in specs:
        build_commands = specs["build"]
        if isinstance(build_commands, str):
            build_commands = [build_commands]
        commands.extend(build_commands)
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

    result = "\n".join(cleaned)
    if result and not result.endswith("\n"):
        result += "\n"
    return result, binary_files


def _make_image_download_script(instance: dict) -> str:
    """Generate a COPY instruction to bring in pre-downloaded image_assets."""
    image_assets = instance.get("image_assets")
    if not image_assets:
        return ""
    if isinstance(image_assets, str):
        image_assets = json.loads(image_assets) if image_assets else {}

    has_assets = (
        image_assets.get("test_patch")
        or image_assets.get("problem_statement")
        or image_assets.get("patch")
    )
    if not has_assets:
        return ""

    instance_id = instance["instance_id"]
    return f"COPY src/image_assets/{instance_id}/ /swebench/image_assets/"


def _get_dockerfile(instance) -> str:
    repo = instance["repo"]
    version = instance.get("version") or None
    base_commit = instance["base_commit"]
    specs = MAP_REPO_VERSION_TO_SPECS_JS[repo][version]
    dockerfile = _DOCKERFILE_BASE_JS
    docker_specs = specs.get("docker_specs", {})
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
    pre_install_script = make_pre_install_script(specs)
    if pre_install_script:
        dockerfile += f"\n{pre_install_script}\n"
    repo_script = make_repo_script_list(specs, repo, base_commit)
    if repo_script:
        dockerfile += f"\n{repo_script}\n"
    # Download image_assets at build time
    image_script = _make_image_download_script(instance)
    if image_script:
        dockerfile += f"\n{image_script}\n"
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
    test_cmd = MAP_REPO_VERSION_TO_SPECS_JS[instance["repo"]][instance["version"]]["test_cmd"]
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
    # TWO Chrome binaries per image, used for different test phases:
    #
    #   KARMA_CHROME = /usr/bin/google-chrome-stable (modern, system-wide).
    #     Karma WebGL tests (ol.layer.Heatmap) crash in era-matched Chromium
    #     because 2019–2022 snapshots don't have working ANGLE/SwiftShader
    #     support. Modern Chrome does, with customLaunchers flags.
    #
    #   RENDERING_CHROME = /opt/chromium/chrome (era-matched to this version's
    #     puppeteer — see _OL_CHROMIUM_PINS in constants.py). Puppeteer
    #     rendering tests compare screenshots against expected.png
    #     pixel-for-pixel; any browser drift → pixel diff failures.
    KARMA_CHROME = "PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable"
    RENDERING_CHROME = "PUPPETEER_EXECUTABLE_PATH=/opt/chromium/chrome"
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    SSL_LEGACY = "NODE_OPTIONS=--openssl-legacy-provider"
    cmds = []
    for test_path in _get_test_paths(instance):
        test_type = test_path.split('/')[1] if '/' in test_path else ""
        if test_type == "browser":
            cmds.append(f'{KARMA_CHROME} {XVFB} su chromeuser -c "npm run test-browser"')
        elif test_type == "rendering":
            # CI=true activates puppeteer's --no-sandbox args (required in Docker).
            # --log-level=info emits "ok" lines for passing cases.
            # --force skips getOutdated() filter so ALL cases run.
            PENV = f"CI=true {RENDERING_CHROME}"
            if instance.get("version") in ['7.4']:
                # v7.4 needs a rollup build first (build-full) to produce ol.js.
                cmds.append(
                    f'{PENV} {XVFB} su chromeuser -c "'
                    f'{PENV} npm run build-full && {PENV} node test/rendering/test.js --force --log-level=info"'
                )
            else:
                cmds.append(
                    f'{PENV} {XVFB} su chromeuser -c '
                    f'"{PENV} npm run test-rendering -- --force --log-level=info"'
                )
        elif test_type == "spec":
            cmds.append(f'{KARMA_CHROME} {XVFB} su chromeuser -c "npm run karma -- --single-run --log-level error"')
        elif test_type == "node":
            # Use mocha's JSON reporter so parser picks up results (default
            # spec reporter tree with ✓/✗ isn't parsed).
            cmds.append("npm run test-node -- --reporter json")
        else:
            cmds.append("npm run test")
        if test_type in ['spec', 'rendering', 'browser'] and instance.get('version') in [
            '6.1', '6.2', '6.3', '6.4', '6.5', '6.5.1', '6.6',
            '4.3', '4.4', '4.5', '4.6', '5.1', '5.2', '5.3'
        ]:
            cmds[-1] = f"{SSL_LEGACY} {cmds[-1]}"
    # Dedupe while preserving insertion order — reproducible eval.sh across bakes.
    return list(dict.fromkeys(cmds))


def _get_test_cmds_next(instance: dict) -> list:
    SET_PUPPETEER = "PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable"
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    # Dedupe while preserving insertion order — reproducible eval.sh across bakes.
    return list(dict.fromkeys([
        f'timeout 5m bash -c \'{SET_PUPPETEER} {XVFB} '
        f'su chromeuser -c "npm run test {test_path.split("/")[1]}"\''
        for test_path in _get_test_paths(instance)
    ]))


def _get_test_cmds_carbon(instance: dict) -> list:
    # Derives yarn-test commands from test_patch paths, normalizes each to a
    # Jest-matchable location, then drops any scope dominated by a broader
    # prefix so parallel Jest runs never overlap. Overlap is what §4.7 of
    # MULTIMODAL_FIXES.md targets: a later broad run can overwrite a narrow
    # run's PASS with a FAIL triggered by the achecker cache race.
    max_workers = " --maxWorkers=1" if instance.get("version") == "12" else ""
    test_paths: list[str] = []
    standalone_cmds: list[str] = []

    for test_path in _get_test_paths(instance):
        # Snapshot files aren't runnable — point Jest at the component dir.
        if re.search(r"__snapshots__/(.*).js.snap$", test_path):
            test_path = "/".join(test_path.split("/")[:-2])
        # __tests__/foo-test.js → parent dir (Jest resolves by directory).
        if "__tests__" in test_path:
            test_path = test_path.split("__tests__")[0]
        # packages/*/src/components/*/next/* isn't file-matched by Jest —
        # fall back to the component directory.
        if "/next/" in test_path and "/components/" in test_path:
            test_path = test_path.split("/next/")[0]
        # cra-template/template/* is a standalone CRA scaffold: its deps
        # aren't in package.json and files don't import React. Patch deps
        # in, yarn install, then run jest with an inline config that
        # enables the automatic JSX runtime. Self-contained — skips dedup.
        if "cra-template/template/" in test_path:
            standalone_cmds.append(
                "node -e '"
                'const p=require("./packages/cra-template/package.json");'
                'p.dependencies={"@apollo/client":"3.7.4","react-router-dom":"6.6.2",'
                '"@testing-library/react":"12.1.5","@testing-library/jest-dom":"5.16.5",'
                '"@testing-library/user-event":"12.8.3","graphql":"16.6.0",'
                '"react":"17.0.1","react-dom":"17.0.1"};'
                'require("fs").writeFileSync("packages/cra-template/package.json",JSON.stringify(p,null,2));'
                "' && yarn install 2>&1 | tail -3 ; "
                'npx jest --no-colors --json '
                """--config '{"preset":"jest-config-carbon","transform":{"^.+\\\\.(js|jsx)$":["babel-jest",{"presets":["@babel/preset-env",["@babel/preset-react",{"runtime":"automatic"}]]}]}}' """
                'packages/cra-template/template/src'
            )
            continue
        # .e2e.js isn't file-matched by `yarn test` — containing dir instead.
        if test_path.endswith(".e2e.js"):
            test_path = "/".join(test_path.split("/")[:-1]) + "/"
        # Normalize directory-ish paths with a trailing slash so the prefix
        # dedup below can distinguish dirs (which dominate) from files.
        if not test_path.endswith((".js", ".ts", ".jsx", ".tsx", "/")):
            test_path = test_path + "/"
        test_paths.append(test_path)

    # Prefix dedup: if A is a directory scope that's a strict prefix of B,
    # running A already runs everything under B — drop B. Sort by length
    # (shortest first) so each broader scope is seen before its extensions.
    kept: list[str] = []
    for p in sorted(set(test_paths), key=len):
        if any(k.endswith("/") and p.startswith(k) and p != k for k in kept):
            continue
        kept.append(p)

    yarn_cmds = [f"yarn test --json{max_workers} {p}" for p in kept]
    return list(dict.fromkeys(standalone_cmds + yarn_cmds))


def _get_test_cmds_scratch_gui(instance: dict) -> list:
    test_prefix = MAP_REPO_VERSION_TO_SPECS_JS[instance['repo']][instance['version']]["test_cmd"]
    cmds = []
    for test_path in _get_test_paths(instance):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        cmds.append(f"{test_prefix} {test_path}")
    # Dedupe while preserving insertion order — reproducible eval.sh across bakes.
    return list(dict.fromkeys(cmds))


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
    # Dedupe while preserving insertion order — reproducible eval.sh across bakes.
    return list(dict.fromkeys(cmds))


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
    # Dedupe while preserving insertion order — reproducible eval.sh across bakes.
    return list(dict.fromkeys(cmds))


def _get_test_cmds_react_pdf(instance: dict) -> list:
    # Run the full test suite (not narrowed to the test_patch's package) so
    # P2P entries in other packages (textkit, image, stylesheet, ...) are
    # actually evaluated. Previously: jest was passed "packages/<name>" which
    # made jest skip the rest of the monorepo.
    test_prefix = MAP_REPO_VERSION_TO_SPECS_JS[instance['repo']][instance['version']]["test_cmd"]
    return [test_prefix]


def _get_test_cmds_quarto(instance: dict) -> list[str]:
    """Quarto: direct-render for 5292, tufte-pdf removal for all others."""
    if instance["instance_id"] == "quarto-dev__quarto-cli-5292":
        def _render_block(label: str) -> str:
            m = re.match(r"\[smoke\] > quarto render (\S+) --to (\S+)", label)
            assert m, f"unrecognised 5292 test label: {label}"
            target = "tests/" + m.group(1)
            fmt = m.group(2)
            return (
                f"cd /testbed && if quarto render {target} --to {fmt} 2>/dev/null ; "
                f"then printf '{label} ... \\033[32mok\\033[0m\\n' ; "
                f"else printf '{label} ... \\033[31mFAILED\\033[0m\\n' ; fi"
            )
        f2p_list = instance.get("FAIL_TO_PASS", [])
        if isinstance(f2p_list, str):
            f2p_list = json.loads(f2p_list)
        p2p_list = instance.get("PASS_TO_PASS", [])
        if isinstance(p2p_list, str):
            p2p_list = json.loads(p2p_list)
        parts = ["rm -f tests/docs/page-layout/tufte-pdf.qmd"]
        parts.extend(_render_block(t) for t in f2p_list)
        parts.extend(_render_block(t) for t in p2p_list)
        return parts

    # All other quarto instances: prepend tufte-pdf removal to standard test_cmd
    specs = MAP_REPO_VERSION_TO_SPECS_JS[instance["repo"]][instance.get("version") or None]
    test_cmd = specs["test_cmd"]
    if isinstance(test_cmd, list):
        test_cmd = list(test_cmd)
    else:
        test_cmd = [test_cmd]
    return ["rm -f tests/docs/page-layout/tufte-pdf.qmd"] + test_cmd


_CHART_JS_AUTO_LOADED_STEMS = {
    "controller.bar", "controller.bubble", "controller.doughnut",
    "controller.line", "controller.polarArea", "controller.radar",
    "controller.scatter", "core.animation", "core.animations",
    "core.animator", "core.controller", "core.datasetController",
    "core.defaults", "core.element",
}


def _get_test_cmds_chart_js(instance: dict) -> list:
    """Conditionally narrow karma via --grep for spec files not auto-loaded.

    Karma's rollup bundle only executes the alphabetically first ~14 spec
    files. If the test_patch only touches files in that set, the default
    (no --grep) run works and is more reliable (fixture auto-tests load).
    Only add --grep runs for spec stems OUTSIDE the auto-loaded set.
    """
    test_cmd_list = MAP_REPO_VERSION_TO_SPECS_JS[instance["repo"]][instance["version"]]["test_cmd"]
    greps = set()
    for path in _get_test_paths(instance):
        if path.startswith("test/specs/") and path.endswith(".tests.js"):
            greps.add(path[len("test/specs/"):-len(".tests.js")])
        elif path.startswith("test/fixtures/"):
            stem = path[len("test/fixtures/"):].split("/", 1)[0]
            if stem:
                greps.add(stem)
    # Only grep for stems NOT in the auto-loaded set
    extra_greps = greps - _CHART_JS_AUTO_LOADED_STEMS
    if not extra_greps:
        return test_cmd_list
    base_cmds = [c for c in test_cmd_list if "karma start" not in c]
    karma_cmds = [c for c in test_cmd_list if "karma start" in c]
    # Run full suite first (covers auto-loaded stems), then per-file for extras
    result = list(test_cmd_list)
    for grep in sorted(extra_greps):
        for cmd in karma_cmds:
            result.append(cmd.replace("--grep ", f"--grep {grep} "))
    return result


def _get_test_cmds_p5js(instance: dict) -> list:
    """Conditionally re-run yuidoc before tests.

    Only needed when the gold patch touches docs/preprocessor.js (e.g. 4561
    adds parameterData.json generation). Running yuidoc unconditionally
    regenerates doc data and changes which doc-example tests exist, causing
    spurious P2P drift on other instances.
    """
    specs = MAP_REPO_VERSION_TO_SPECS_JS[instance["repo"]][instance["version"]]
    test_cmd = specs["test_cmd"]
    if isinstance(test_cmd, list):
        cmds = list(test_cmd)
    else:
        cmds = [test_cmd]
    all_paths = _get_test_paths(instance) + re.findall(
        r"diff --git a/.* b/(.*)", instance.get("patch", "")
    )
    if any("docs/preprocessor" in p for p in all_paths):
        cmds.insert(0, "./node_modules/.bin/grunt yui --force || true")
    return cmds


_MAP_REPO_TO_TEST_CMDS = {
    "alibaba-fusion/next": _get_test_cmds_next,
    "carbon-design-system/carbon": _get_test_cmds_carbon,
    "chartjs/Chart.js": _get_test_cmds_chart_js,
    "GoogleChrome/lighthouse": _get_test_cmds_lighthouse,
    "openlayers/openlayers": _get_test_cmds_openlayers,
    "prettier/prettier": _get_test_cmds_prettier,
    "PrismJS/prism": _get_test_cmds_prism,
    "quarto-dev/quarto-cli": _get_test_cmds_quarto,
    # scratch-gui: static test_cmd runs all jest tests, works fine.
    # Per-instance cmd is too narrow (misses F2P tests not in test_patch).
    "diegomura/react-pdf": _get_test_cmds_react_pdf,
    "processing/p5.js": _get_test_cmds_p5js,
}


def _get_test_commands(instance: dict, specs: dict) -> str:
    """Get test command(s) for an instance. Uses per-repo handler if available."""
    repo = instance["repo"]
    if repo in _MAP_REPO_TO_TEST_CMDS:
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
        "git status > /dev/null 2>&1",
        "git show > /tmp/git_show.log 2>&1",
        f"git -c core.fileMode=false diff {base_commit} > /tmp/git_diff.log 2>&1",
    ]

    # Per-repo/version eval setup from specs (env prep before tests)
    eval_commands.extend(specs.get("eval_setup", []))

    # Carbon: rebuild when gold patch touches source (instance-specific, can't be in specs)
    if repo == "carbon-design-system/carbon" and re.search(
        r"^diff --git a/packages/[^/]+/src/",
        instance.get("patch", "") or "",
        re.MULTILINE,
    ):
        eval_commands.append("yarn build 2>&1 | tail -5 || true")

    if test_patch:
        # Strip binary diffs — they can't be applied via heredoc
        clean_test_patch, binary_files = _strip_binary_diffs(test_patch)

        # Extract both a/ and b/ sides of each diff header
        a_sides = re.findall(r"diff --git a/(.*) b/.*", test_patch)
        b_sides = re.findall(r"diff --git a/.* b/(.*)", test_patch)

        # Detect new files (need rm, not checkout)
        new_file_markers = set()
        lines = test_patch.split("\n")
        for i, line in enumerate(lines):
            if "new file mode" in line:
                for j in range(max(0, i - 2), i):
                    m = re.match(r"diff --git a/.* b/(.*)", lines[j])
                    if m:
                        new_file_markers.add(m.group(1))
                        break

        # Build reset command handling renames correctly:
        # - Regular files (a == b): git checkout a/ side
        # - Renames (a != b): git checkout a/ side + rm b/ side
        # - New files: rm b/ side
        checkout_files = []
        rm_files = list(new_file_markers)
        for a, b in zip(a_sides, b_sides):
            if b in new_file_markers:
                continue  # already handled
            if a != b:
                # Rename: restore old name, remove new name
                checkout_files.append(a)
                rm_files.append(b)
            else:
                checkout_files.append(a)

        reset_parts = []
        if checkout_files:
            reset_parts.append(f"git checkout {base_commit} {' '.join(checkout_files)}")
        if rm_files:
            reset_parts.append(f"rm -f {' '.join(rm_files)}")
        reset_tests_command = " && ".join(reset_parts) if reset_parts else "true"

        eval_commands.append(reset_tests_command)

        # Apply text-only portion of test_patch
        if clean_test_patch.strip():
            HEREDOC_DELIMITER = "EOF_114329324912"
            apply_test_patch_command = (
                f"git apply -v - <<'{HEREDOC_DELIMITER}'\n{clean_test_patch}\n{HEREDOC_DELIMITER}"
            )
            eval_commands.append(apply_test_patch_command)

        # Restore binary files from build-time staging dir.
        # `cp -a` copies attributes from the staging source (typically 775 root:root),
        # clobbering the image's 777 perms on any overlapping dirs. That breaks
        # non-root users (chromeuser, uid 1000) writing siblings (e.g. Puppeteer's
        # actual.png). Restore world-writable after cp.
        if binary_files:
            eval_commands.append(
                "test -d /swebench/image_assets/test_patch && "
                "cp -a /swebench/image_assets/test_patch/. /testbed/ 2>/dev/null || true"
            )
            eval_commands.append("chmod -R a+rwX /testbed 2>/dev/null || true")

    eval_commands += [
        f": '{START_TEST_OUTPUT}'",
        test_command,
    ]
    # Force stdout flush before the END marker. Without this, buffered test
    # output (e.g. mocha JSON at 9MB+) can arrive after END and be cut off by
    # the grader's START/END slice. Hits eslint, quarto, and any large suite.
    eval_commands.append("{ set +x ; } 2>/dev/null ; sync ; sleep 0.1 ; set -x")
    eval_commands.append(f": '{END_TEST_OUTPUT}'")

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


def generate_instances(
    dataset_name_or_path: str,
    split: str = "test",
    output_dir: str = "src/instances",
    instance_ids: list[str] | None = None,
):
    """Generate Dockerfiles for each instance."""
    instances = load_instances(dataset_name_or_path, split, instance_ids)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for instance in instances:
        dockerfile_path = output_path / f"{instance['instance_id']}.Dockerfile"
        dockerfile_path.write_text(_get_dockerfile(instance))

    print(f"Generated {len(instances)} Dockerfiles in {output_path}")


def main():
    parser = ArgumentParser(
        description="Generate Dockerfiles for SWE-bench Multimodal (JavaScript benchmarks)"
    )
    parser.add_argument(
        "dataset",
        help="HuggingFace dataset name or path to local JSON/JSONL file",
    )
    parser.add_argument("--split", default="test")
    parser.add_argument("--output_dir", default="src/instances")
    parser.add_argument("--instance_ids", nargs="+", default=None)
    args = parser.parse_args()
    generate_instances(args.dataset, args.split, args.output_dir, args.instance_ids)


if __name__ == "__main__":
    main()
