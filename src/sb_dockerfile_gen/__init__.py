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
# Fonts + dbus bits previously piggy-backed onto the google-chrome-stable
# install. CJK fonts are required for pixel-diff rendering tests that compare
# against pre-rendered PNGs containing non-Latin glyphs. Each repo that needs
# a browser pins its own Chromium via chromium_preinstall or analogous
# pre_install step (bpmn-js, next, lighthouse, p5.js, openlayers, chart.js).
RUN apt-get update && apt-get install -y \
    fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
    fonts-khmeros fonts-kacst fonts-freefont-ttf \
    libxss1 dbus-x11 \
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


# OpenLayers needs an older Mesa (21.x) for headless WebGL software-rendering
# to work with the era-matched Chromium versions its puppeteer pins to.
# jammy ships Mesa 23.x which silently breaks Chromium 97-121 WebGL → tests
# abort at ol/layer/Heatmap. Ubuntu 20.04's Mesa 21.2 has been verified to
# run the full karma suite with just `--no-sandbox`. This template skips the
# system Chrome install entirely and lets puppeteer download its own
# Chromium during `npm install` (PUPPETEER_SKIP_DOWNLOAD intentionally unset).
_DOCKERFILE_BASE_JS_OL = r"""
FROM --platform=linux/amd64 ubuntu:20.04

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

ENV NVM_DIR /usr/local/nvm

RUN mkdir -p $NVM_DIR
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.3/install.sh | bash
RUN apt-get update && apt-get install -y \
    procps \
    xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable \
    xfonts-cyrillic x11-apps \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdrm2 \
    libgbm1 libgconf-2-4 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 \
    libnss3 libpango-1.0-0 libpangocairo-1.0-0 libxcomposite1 \
    libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 libxss1 libxshmfence1 libglu1 \
    libgl1-mesa-dri libegl1-mesa libxtst6 \
    fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg \
    fonts-khmeros fonts-kacst fonts-freefont-ttf \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/dbus

ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/run/dbus/system_bus_socket"

RUN dbus-daemon --system --fork

ENV OPENSSL_CONF /etc/ssl

# Puppeteer 19.7+ caches its bundled Chromium in $PUPPETEER_CACHE_DIR (defaults
# to ~/.cache/puppeteer). Pin it to a shared, world-readable location so karma
# (running as chromeuser) can use the same binary that npm install (root)
# downloaded — without copying the cache across users.
ENV PUPPETEER_CACHE_DIR=/opt/puppeteer-cache
RUN mkdir -p /opt/puppeteer-cache && chmod 0777 /opt/puppeteer-cache

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
    # OpenLayers gets its own vintage base (Ubuntu 20.04, no system Chrome,
    # puppeteer-bundled Chromium) so headless WebGL software-rendering works
    # against era-matched Chromium. See _DOCKERFILE_BASE_JS_OL above.
    dockerfile = _DOCKERFILE_BASE_JS_OL if repo == "openlayers/openlayers" else _DOCKERFILE_BASE_JS
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
    # Per-spec ENV vars (e.g. PUPPETEER_SKIP_DOWNLOAD for OL puppeteer-21+ pins
    # to avoid the BuildKit npm install hang on the puppeteer download hook).
    for env_key, env_value in docker_specs.get("env", {}).items():
        dockerfile += f"ENV {env_key}={env_value}\n"
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


# Per-instance test command generation has moved into the per-repo SPECS
# modules under sb_dockerfile_gen/specs/. A SPECS_X[v]["test_cmd"] entry is
# either a string, a list[str], or a callable(instance) -> list[str] —
# `_get_test_commands` below handles all three.



def _get_test_commands(instance: dict, specs: dict) -> str:
    """Resolve a spec's test_cmd to a single shell string.

    `test_cmd` may be a string, a list[str], or a callable(instance) -> list[str].
    Multi-command results are joined with `;` so all test runs execute even if
    one fails (we need output from every test for F2P/P2P grading).
    """
    test_cmd = specs["test_cmd"]
    if callable(test_cmd):
        cmds = test_cmd(instance)
        return " ; ".join(cmds) if cmds else ""
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

    # Per-repo/version eval setup from specs. May be a list[str] or a
    # callable(instance) -> list[str] for instance-conditional setup.
    eval_setup = specs.get("eval_setup", [])
    if callable(eval_setup):
        eval_setup = eval_setup(instance)
    eval_commands.extend(eval_setup)

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
