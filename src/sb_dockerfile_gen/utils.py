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
        # Full clone (all branches). Fast for most repos (< 2 min).
        # --single-branch was faster but fails when base_commit is on a non-default branch.
        clone_cmd = f"git clone -o origin https://github.com/{repo} {workdir}"
    return [
        clone_cmd,
        f"cd {workdir}",
        f"git reset --hard {base_commit}",
        "git remote remove origin",
        # Unconditionally delete all non-HEAD branches and ALL tags. Timestamp-gated
        # tag deletion misses tags pointing to commits that predate base_commit but sit
        # on branches whose tips are after base_commit — those tags keep future commits
        # reachable (see multilingual d2cf82d / swe-bench issue #465).
        "git branch | grep -v '^\\*' | xargs -r git branch -D || true",
        "git tag -l | xargs -r git tag -d",
        "git reflog expire --expire=now --all",
        # Prune unreachable objects so future commits cannot be recovered via
        # `git fsck --lost-found` or `git cat-file -p <sha>`.
        "git gc --prune=now --aggressive",
        # Verify no future commits remain reachable.
        f"TARGET_EPOCH=$(git show -s --format=%ct {base_commit})",
        'AFTER_EPOCH=$((TARGET_EPOCH + 1))',
        'AFTER_TIMESTAMP=$(date -u -d "@$AFTER_EPOCH" "+%Y-%m-%d %H:%M:%S")',
        'COMMIT_COUNT=$(git log --oneline --all --since="$AFTER_TIMESTAMP" | wc -l)',
        '[ "$COMMIT_COUNT" -eq 0 ] || exit 1',
        "cd - || true",
        # chmod after git reset so permissions aren't reverted by git
        f"chmod -R 777 {workdir}",
    ]


def get_modified_files(patch: str) -> list[str]:
    """Get the list of modified files in a patch."""
    from unidiff import PatchSet

    source_files = [
        f.source_file for f in PatchSet(patch) if f.source_file != "/dev/null"
    ]
    return [x[2:] for x in source_files if x.startswith("a/")]
