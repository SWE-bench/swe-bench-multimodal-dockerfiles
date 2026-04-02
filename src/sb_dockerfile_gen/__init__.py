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


def _get_dockerfile(instance) -> str:
    repo = instance["repo"]
    version = instance.get("version")
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
    repo_script = make_repo_script_list(specs, repo, base_commit)
    if repo_script:
        dockerfile += f"\n{repo_script}\n"
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
            cmds.append(f'{SET_PUPPETEER} {XVFB} su chromeuser -c "npm run test-rendering"')
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
    return list(set(cmds))


def _get_test_cmds_next(instance: dict) -> list:
    SET_PUPPETEER = "PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable"
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    return list(set([
        f'timeout 5m bash -c \'{SET_PUPPETEER} {XVFB} '
        f'su chromeuser -c "npm run test {test_path.split("/")[1]}"\''
        for test_path in _get_test_paths(instance)
    ]))


def _get_test_cmds_carbon(instance: dict) -> list:
    cmds = []
    for test_path in _get_test_paths(instance):
        if re.search(r"__snapshots__/(.*).js.snap$", test_path):
            test_path = "/".join(test_path.split("/")[:-2])
        if "__tests__" in test_path:
            test_path = test_path.split("__tests__")[0]
        # For paths under packages/*/src/components/*/next/ or packages/cra-template/,
        # Jest won't match the specific file. Target the component directory instead.
        if "/next/" in test_path and "/components/" in test_path:
            test_path = test_path.split("/next/")[0]
        if "cra-template/template/" in test_path:
            test_path = "packages/cra-template"
        # e2e test files (.e2e.js) are not matched by Jest — target the component directory
        if test_path.endswith(".e2e.js"):
            test_path = "/".join(test_path.split("/")[:-1])
        cmds.append(f"yarn test {test_path}")
    return list(set(cmds))


def _get_test_cmds_scratch_gui(instance: dict) -> list:
    test_prefix = MAP_REPO_VERSION_TO_SPECS_JS[instance['repo']][instance['version']]["test_cmd"]
    cmds = []
    for test_path in _get_test_paths(instance):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        cmds.append(f"{test_prefix} {test_path}")
    return list(set(cmds))


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
    return list(set(cmds))


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
    return list(set(cmds))


def _get_test_cmds_react_pdf(instance: dict) -> list:
    test_prefix = MAP_REPO_VERSION_TO_SPECS_JS[instance['repo']][instance['version']]["test_cmd"]
    cmds = []
    for test_path in _get_test_paths(instance):
        if test_path.endswith(".png"):
            continue
        elif test_path.startswith("packages/"):
            test_path = "/".join(test_path.split("/")[:2])
            cmds.append(f"{test_prefix} {test_path}")
        elif test_path.startswith("tests/"):
            cmds.append(test_prefix)
    return list(set(cmds))


_MAP_REPO_TO_TEST_CMDS = {
    "alibaba-fusion/next": _get_test_cmds_next,
    "carbon-design-system/carbon": _get_test_cmds_carbon,
    "GoogleChrome/lighthouse": _get_test_cmds_lighthouse,
    "openlayers/openlayers": _get_test_cmds_openlayers,
    "prettier/prettier": _get_test_cmds_prettier,
    "PrismJS/prism": _get_test_cmds_prism,
    # scratch-gui: static test_cmd runs all jest tests, works fine.
    # Per-instance cmd is too narrow (misses F2P tests not in test_patch).
    "diegomura/react-pdf": _get_test_cmds_react_pdf,
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
    version = instance.get("version")
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

    if test_patch:
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

        HEREDOC_DELIMITER = "EOF_114329324912"
        apply_test_patch_command = (
            f"git apply -v - <<'{HEREDOC_DELIMITER}'\n{test_patch}\n{HEREDOC_DELIMITER}"
        )
        eval_commands += [reset_tests_command, apply_test_patch_command]

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
