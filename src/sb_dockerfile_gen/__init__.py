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


# ── Eval script generation ─────────────────────────────────────────────


def _get_eval_script(instance: dict) -> str:
    """Generate the eval.sh script for a multimodal instance."""
    repo = instance["repo"]
    version = instance.get("version")
    base_commit = instance["base_commit"]
    test_patch = instance.get("test_patch", "")
    specs = MAP_REPO_VERSION_TO_SPECS_JS[repo][version]

    test_cmd = specs["test_cmd"]
    if isinstance(test_cmd, list):
        test_command = " && ".join(test_cmd)
    else:
        test_command = test_cmd

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
        reset_tests_command = f"git checkout {base_commit} {' '.join(test_files)}"

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
