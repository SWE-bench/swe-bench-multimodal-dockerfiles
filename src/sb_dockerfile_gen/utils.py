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
        # Fetch just the base commit. A full clone bakes every historical version of
        # committed artifacts into the image -- carbon's .git alone is 7.8GB of a 9.2GB
        # /testbed because Yarn zero-installs commits dependency zips. Falls back to a
        # full clone if the host refuses a by-SHA fetch.
        clone_cmd = (
            f"(mkdir -p {workdir} && cd {workdir} && git init -q . "
            f"&& git remote add origin https://github.com/{repo} "
            f"&& git fetch -q --depth 1 origin {base_commit} "
            f"&& git reset -q --hard FETCH_HEAD) "
            f"|| (rm -rf {workdir} && git clone -o origin https://github.com/{repo} {workdir})"
        )
    return [
        clone_cmd,
        f"chmod -R 777 {workdir}",
        f"cd {workdir}",
        f"git reset --hard {base_commit}",
        "git remote remove origin",
        # Remove all future information (tags/branches/objects newer than base).
        f"TARGET_TIMESTAMP=$(git show -s --format=%ci {base_commit})",
        # Delete every tag and branch: matches the multilingual generator, and is
        # simpler than pruning by date (the previous `git tag -l | while read`
        # form silently stopped after ~29 of 257 tags because a git command in
        # the loop body consumed the piped stdin).
        "git branch | grep -v '^\\*' | xargs -r git branch -D || true",
        "git tag -l | xargs -r git tag -d",
        "git reflog expire --expire=now --all",
        # Physically drop the now-unreachable future commits; without this they
        # stay in the pack and are readable via git cat-file / fsck.
        "git gc --prune=now --aggressive",
        # Fail the build if anything newer than the base commit survived, so a
        # broken prune can never ship as a silently leaky image.
        "AFTER_TIMESTAMP=$(date -d \"$TARGET_TIMESTAMP + 1 second\" '+%Y-%m-%d %H:%M:%S')",
        'COMMIT_COUNT=$(git log --oneline --all --since="$AFTER_TIMESTAMP" | wc -l)',
        '[ "$COMMIT_COUNT" -eq 0 ] || exit 1',
        "cd - || true",
    ]


def get_modified_files(patch: str) -> list[str]:
    """Get the list of modified files in a patch."""
    from unidiff import PatchSet

    source_files = [
        f.source_file for f in PatchSet(patch) if f.source_file != "/dev/null"
    ]
    return [x[2:] for x in source_files if x.startswith("a/")]
