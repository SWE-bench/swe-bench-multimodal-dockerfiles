"""Mirror the binary assets a task's tests need.

Some tasks compare rendering against a baseline image, which a text patch cannot
carry. The dataset lists those files under ``image_assets`` as {path, url} pairs,
and the harness stages them into the container after applying the patch.

Keeping a copy with the task means an evaluation does not depend on a url still
being reachable years later. Assets live at ``tasks/<instance_id>/assets/<path>``,
mirroring where they land in the repository under test.

    python -m dockerfile_gen.assets                 # fetch whatever is missing
    python -m dockerfile_gen.assets --force         # re-download everything
    python -m dockerfile_gen.assets -i <instance_id>
"""

from __future__ import annotations

import urllib.request
from argparse import ArgumentParser
from pathlib import Path

from .tasks import TASKS_DIR, load_task, task_dirs

TIMEOUT = 60


def _entries(instance: dict) -> list[dict]:
    """The assets staged at eval time, which is only the test_patch ones.

    problem_statement assets are model-facing images in the issue text; they are
    never placed in the container, so there is nothing to mirror.
    """
    assets = instance.get("image_assets") or {}
    return [e for e in assets.get("test_patch") or [] if e.get("path") and e.get("url")]


def fetch_assets(
    tasks_dir: Path = TASKS_DIR,
    instance_ids: list[str] | None = None,
    force: bool = False,
) -> tuple[int, int, list[str]]:
    wanted = set(instance_ids or [])
    fetched = skipped = 0
    failed: list[str] = []

    for task_dir in task_dirs(tasks_dir):
        if wanted and task_dir.name not in wanted:
            continue
        for entry in _entries(load_task(task_dir)):
            dest = task_dir / "assets" / entry["path"]
            if dest.is_file() and not force:
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                with urllib.request.urlopen(entry["url"], timeout=TIMEOUT) as resp:
                    dest.write_bytes(resp.read())
                fetched += 1
            except Exception as e:  # noqa: BLE001 - report every failure, keep going
                failed.append(f"{task_dir.name} {entry['path']}: {type(e).__name__} {e}")
    return fetched, skipped, failed


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--instance", dest="instance_ids", nargs="+", default=None)
    parser.add_argument("--force", action="store_true", help="re-download existing files")
    args = parser.parse_args()

    fetched, skipped, failed = fetch_assets(
        instance_ids=args.instance_ids, force=args.force
    )
    print(f"fetched {fetched}, already present {skipped}, failed {len(failed)}")
    for line in failed:
        print(f"  {line}")
