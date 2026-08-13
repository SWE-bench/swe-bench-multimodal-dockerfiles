"""Mirror the binary assets a dataset's patches reference.

A text patch cannot carry binary files, so the dataset lists them in
``image_assets`` as {path, url} pairs. Fetching those urls at evaluation time
makes every run depend on the upstream host still serving them, so we keep a
copy here, next to the Dockerfiles -- these are dataset-specific assets, and
the harness stays dataset-agnostic by looking them up by instance_id/path.

``problem_statement`` assets are deliberately skipped: they are model-facing
inputs, not something the container needs.

Usage:
    python -m sb_dockerfile_gen.assets SWE-bench/SWE-bench_Multimodal \\
        --split test --output-dir src/assets
"""

from __future__ import annotations

import json
import urllib.request
from argparse import ArgumentParser
from pathlib import Path

# Only patch-borne assets are needed inside the container at eval time.
EVAL_ASSET_KEYS = ("test_patch", "patch")


def _asset_entries(instance: dict) -> list[dict]:
    raw = instance.get("image_assets")
    if not raw:
        return []
    assets = json.loads(raw) if isinstance(raw, str) else raw
    if not isinstance(assets, dict):
        return []
    out = []
    for key in EVAL_ASSET_KEYS:
        for entry in assets.get(key) or []:
            if entry.get("path") and entry.get("url"):
                out.append(entry)
    return out


def fetch_assets(
    dataset_name: str,
    split: str = "test",
    output_dir: str = "src/assets",
    force: bool = False,
) -> tuple[int, int]:
    """Download eval-time assets into ``output_dir/<instance_id>/<path>``.

    Returns (fetched, skipped).
    """
    from datasets import load_dataset

    dataset = load_dataset(dataset_name, split=split)
    out = Path(output_dir)
    fetched = skipped = 0
    for instance in dataset:
        for entry in _asset_entries(instance):
            dest = out / instance["instance_id"] / entry["path"]
            if dest.exists() and not force:
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(entry["url"], timeout=60) as resp:
                dest.write_bytes(resp.read())
            fetched += 1
    return fetched, skipped


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("dataset", help="HuggingFace dataset name or local path")
    parser.add_argument("--split", default="test")
    parser.add_argument("--output-dir", default="src/assets")
    parser.add_argument("--force", action="store_true", help="re-download existing files")
    args = parser.parse_args()
    fetched, skipped = fetch_assets(
        args.dataset, args.split, args.output_dir, args.force
    )
    print(f"Fetched {fetched} assets ({skipped} already present) into {args.output_dir}")


if __name__ == "__main__":
    main()
