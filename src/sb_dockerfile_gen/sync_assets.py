"""Sync image_assets from mm-resources into src/image_assets/<instance_id>/.

Reads each instance's metadata.json from mm-resources to map flat filenames
back to the proper directory hierarchy expected by the Dockerfile COPY and
eval scripts.  Falls back to ``__`` unflattening for files not listed in
metadata.

Usage:
    python src/sb_dockerfile_gen/sync_assets.py /path/to/mm-resources/resources
    python src/sb_dockerfile_gen/sync_assets.py /path/to/mm-resources/resources \\
        --instance_ids chartjs__Chart.js-10157
"""

import json
import logging
import shutil
from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import unquote, urlparse

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

_DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent.parent / "src" / "image_assets"

# Asset categories that use repo-relative paths inside the container.
_PATH_CATEGORIES = {"test_patch", "patch"}


def _proper_path_from_url(url: str, category: str) -> str:
    """Derive the proper output path from a URL and asset category.

    - test_patch / patch: repo-relative path from raw.githubusercontent.com URL
    - problem_statement: bare filename (matches original _sanitize_filename)
    """
    if category in _PATH_CATEGORIES:
        # URL: https://raw.githubusercontent.com/owner/repo/commit/path/to/file.ext
        #       0      1  2                       3     4    5      6+
        parts = url.split("/")
        if "raw.githubusercontent.com" in url and len(parts) > 6:
            return "/".join(parts[6:])
        # Fallback for non-GitHub URLs
        parsed = urlparse(url)
        return unquote(parsed.path.rstrip("/").split("/")[-1])

    # problem_statement (and any other category): bare filename
    parsed = urlparse(url)
    name = unquote(parsed.path.rstrip("/").split("/")[-1])
    return name or "unknown"


def _unflatten_name(flat_name: str, category: str) -> str:
    """Unflatten a ``__``-separated filename back to a path.

    - test_patch / patch: ``a__b__c.png`` → ``a/b/c.png``
    - problem_statement: ``12345__file.png`` → ``file.png``  (strip numeric prefix)
                         ``file.png`` → ``file.png``         (no prefix)
    """
    if category in _PATH_CATEGORIES:
        return flat_name.replace("__", "/")

    # problem_statement: the original filename is always the last URL path
    # segment.  mm-resources may prefix with path components joined by __
    # (e.g. "22080__file.png" or "images__tutorials__file.png").
    # Take the last __ segment to recover the bare filename.
    if "__" in flat_name:
        return flat_name.rsplit("__", 1)[-1]
    return flat_name


def sync_from_resources(
    resources_dir: str | Path,
    output_dir: str | Path | None = None,
    instance_ids: list[str] | None = None,
):
    """Sync image assets from mm-resources to src/image_assets/.

    For each instance directory in *resources_dir* that contains a
    metadata.json, copy files into *output_dir*/<instance_id>/ with the
    proper directory hierarchy.

    Uses metadata.json URL mapping when available, falls back to ``__``
    unflattening for files not listed in metadata.
    """
    resources = Path(resources_dir)
    output = Path(output_dir) if output_dir else _DEFAULT_OUTPUT
    output.mkdir(parents=True, exist_ok=True)

    if not resources.is_dir():
        log.error("Resources directory does not exist: %s", resources)
        return

    ids_filter = set(instance_ids) if instance_ids else None
    copied = 0
    skipped = 0
    errors = 0

    for instance_dir in sorted(resources.iterdir()):
        if not instance_dir.is_dir():
            continue
        instance_id = instance_dir.name
        if ids_filter and instance_id not in ids_filter:
            continue

        metadata_path = instance_dir / "metadata.json"
        if not metadata_path.exists():
            continue

        metadata = json.loads(metadata_path.read_text())
        images = metadata.get("images", {})

        # Build reverse map: flat_rel → proper_path (from metadata URLs)
        meta_map: dict[str, str] = {}
        for url, flat_rel in images.items():
            category = flat_rel.split("/")[0]
            flat_name = flat_rel.split("/", 1)[1] if "/" in flat_rel else flat_rel
            proper_name = _proper_path_from_url(url, category)
            meta_map[flat_rel] = f"{category}/{proper_name}"

        out_instance = output / instance_id

        # Walk all files in the instance dir (except metadata.json)
        for src_file in instance_dir.rglob("*"):
            if not src_file.is_file() or src_file.name == "metadata.json":
                continue

            flat_rel = str(src_file.relative_to(instance_dir))

            # Skip non-asset files (reproduction code, etc.)
            category = flat_rel.split("/")[0]
            if category not in ("test_patch", "patch", "problem_statement"):
                continue

            # Determine proper output path
            if flat_rel in meta_map:
                proper_rel = meta_map[flat_rel]
            else:
                # Fallback: unflatten __ separators
                flat_name = flat_rel.split("/", 1)[1] if "/" in flat_rel else flat_rel
                proper_name = _unflatten_name(flat_name, category)
                proper_rel = f"{category}/{proper_name}"

            dest = out_instance / proper_rel

            if dest.exists() and dest.stat().st_size == src_file.stat().st_size:
                skipped += 1
                continue

            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest)
            copied += 1

    log.info("Done: %d copied, %d skipped (exist), %d errors", copied, skipped, errors)


def main():
    parser = ArgumentParser(
        description="Sync image_assets from mm-resources into src/image_assets/"
    )
    parser.add_argument(
        "resources_dir",
        help="Path to mm-resources/resources/ directory",
    )
    parser.add_argument(
        "--output_dir",
        default=None,
        help="Output directory (default: src/image_assets)",
    )
    parser.add_argument(
        "--instance_ids",
        nargs="+",
        default=None,
        help="Only sync these instance IDs",
    )
    args = parser.parse_args()
    sync_from_resources(args.resources_dir, args.output_dir, args.instance_ids)


if __name__ == "__main__":
    main()
