"""
Inlined utilities from swebench — makes this package fully standalone.
"""

from hashlib import blake2b

from sb_dockerfile_gen.constants import REPO_BASE_COMMIT_BRANCH


def generate_heredoc_delimiter(content: str) -> str:
    delimiter = f"EOF_{blake2b(content.encode()).hexdigest()[:12]}"
    while delimiter in content:
        delimiter = (
            f"EOF_{blake2b(content.encode() + delimiter.encode()).hexdigest()[:12]}"
        )
    return delimiter


def make_heredoc_run_command(commands: list[str]) -> str:
    """Create a heredoc-style RUN command from a list of shell commands."""
    if not commands:
        return ""
    heredoc_content = "\n".join(["#!/bin/bash", "set -euxo pipefail", *commands])
    delimiter = generate_heredoc_delimiter(heredoc_content)
    return f"RUN <<{delimiter}\n{heredoc_content}\n{delimiter}\n"


def git_clone_timesafe(repo: str, base_commit: str, workdir: str) -> list[str]:
    """Generate shell commands to clone a repo and remove references to future information."""
    branch = REPO_BASE_COMMIT_BRANCH.get(repo, {}).get(base_commit, "")
    if branch:
        clone_cmd = f"git clone -o origin --branch {branch} --single-branch https://github.com/{repo} {workdir}"
    else:
        # Treeless clone: fetches all commits but downloads blobs on demand.
        # Much faster than full clone, and unlike --single-branch it includes all branches.
        clone_cmd = f"git clone -o origin --filter=blob:none https://github.com/{repo} {workdir}"
    return [
        clone_cmd,
        f"chmod -R 777 {workdir}",
        f"cd {workdir}",
        f"git reset --hard {base_commit}",
        "git remote remove origin",
        # Remove tags newer than base commit (prevents future info leakage)
        f"TARGET_EPOCH=$(git show -s --format=%ct {base_commit})",
        'git tag -l | while read tag; do TAG_COMMIT=$(git rev-list -n 1 "$tag"); TAG_EPOCH=$(git show -s --format=%ct "$TAG_COMMIT"); if [ "$TAG_EPOCH" -gt "$TARGET_EPOCH" ]; then git tag -d "$tag"; fi; done',
        # Delete all branches except the detached HEAD at base_commit
        'git branch -D $(git branch | grep -v "^\\*") 2>/dev/null || true',
        "git reflog expire --expire=now --all",
        "cd - || true",
    ]


def get_modified_files(patch: str) -> list[str]:
    """Get the list of modified files in a patch."""
    from unidiff import PatchSet

    source_files = [
        f.source_file for f in PatchSet(patch) if f.source_file != "/dev/null"
    ]
    return [x[2:] for x in source_files if x.startswith("a/")]
