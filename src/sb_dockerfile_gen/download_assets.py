"""Download image_assets from dataset JSON into src/image_assets/<instance_id>/."""

import json
import logging
import urllib.request
import urllib.error
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse, unquote

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# Repo root default for output
_DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent.parent / "src" / "image_assets"


def _sanitize_filename(url: str) -> str:
    """Extract filename from URL, stripping query strings and fragments."""
    parsed = urlparse(url)
    name = unquote(parsed.path.rstrip("/").split("/")[-1])
    return name or "unknown"


def _download_file(url: str, dest: Path, force: bool) -> bool:
    """Download a single file. Returns True on success."""
    if not force and dest.exists() and dest.stat().st_size > 0:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "swe-bench-asset-dl/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        return True
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        log.warning("Failed %s → %s: %s", url, dest, e)
        return False


def _collect_downloads(instance: dict, output_base: Path) -> list[tuple[str, Path]]:
    """Collect (url, dest_path) pairs for one instance."""
    instance_id = instance["instance_id"]
    ia = instance.get("image_assets")
    if not ia:
        return []
    if isinstance(ia, str):
        ia = json.loads(ia) if ia else {}

    instance_dir = output_base / instance_id
    downloads = []

    # test_patch: list of {path, url}
    test_patch_assets = ia.get("test_patch", [])
    if hasattr(test_patch_assets, "tolist"):
        test_patch_assets = test_patch_assets.tolist()
    for item in test_patch_assets:
        if isinstance(item, str):
            item = json.loads(item)
        path = item.get("path", "")
        url = item.get("url", "")
        if path and url:
            downloads.append((url, instance_dir / "test_patch" / path))

    # problem_statement: list of URL strings
    ps_assets = ia.get("problem_statement", [])
    if hasattr(ps_assets, "tolist"):
        ps_assets = ps_assets.tolist()
    seen_urls = set()
    for url in ps_assets:
        if not isinstance(url, str) or not url or url in seen_urls:
            continue
        seen_urls.add(url)
        fname = _sanitize_filename(url)
        downloads.append((url, instance_dir / "problem_statement" / fname))

    # patch: list of {path, url}
    patch_assets = ia.get("patch", [])
    if hasattr(patch_assets, "tolist"):
        patch_assets = patch_assets.tolist()
    for item in patch_assets:
        if isinstance(item, str):
            item = json.loads(item)
        path = item.get("path", "")
        url = item.get("url", "")
        if path and url:
            downloads.append((url, instance_dir / "patch" / path))

    return downloads


def download_all(
    dataset_path: str,
    output_dir: str | None = None,
    instance_ids: list[str] | None = None,
    force: bool = False,
    workers: int = 16,
):
    """Download all image assets from dataset JSON."""
    output_base = Path(output_dir) if output_dir else _DEFAULT_OUTPUT
    output_base.mkdir(parents=True, exist_ok=True)

    with open(dataset_path) as f:
        data = json.load(f)

    if instance_ids:
        ids = set(instance_ids)
        data = [inst for inst in data if inst["instance_id"] in ids]

    # Collect all downloads
    all_downloads = []
    for inst in data:
        all_downloads.extend(_collect_downloads(inst, output_base))

    if not all_downloads:
        log.info("No assets to download.")
        return

    log.info("Downloading %d files to %s (workers=%d, force=%s)", len(all_downloads), output_base, workers, force)

    ok = 0
    fail = 0
    skip = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {}
        for url, dest in all_downloads:
            if not force and dest.exists() and dest.stat().st_size > 0:
                skip += 1
                continue
            futures[pool.submit(_download_file, url, dest, force)] = (url, dest)

        for future in as_completed(futures):
            if future.result():
                ok += 1
            else:
                fail += 1

    log.info("Done: %d downloaded, %d skipped (exist), %d failed", ok, skip, fail)
    if fail:
        log.warning("%d downloads failed — re-run to retry.", fail)


def main():
    parser = ArgumentParser(description="Download image_assets for SWE-bench Multimodal instances")
    parser.add_argument("dataset", help="Path to swe-bench-mm.json or similar dataset file")
    parser.add_argument("--output_dir", default=None, help="Output directory (default: src/image_assets)")
    parser.add_argument("--instance_ids", nargs="+", default=None, help="Only download for these instances")
    parser.add_argument("--force", action="store_true", help="Re-download even if files exist")
    parser.add_argument("--workers", type=int, default=16, help="Parallel download workers")
    args = parser.parse_args()
    download_all(args.dataset, args.output_dir, args.instance_ids, args.force, args.workers)


if __name__ == "__main__":
    main()
