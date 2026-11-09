"""One-time helper: turns a raw Kaggle "Dogs vs Cats" download into the
backend/data/raw/{cat,dog}/ layout that ml/dataset.py expects.

Handles both common layouts of that dataset:
  1. Flat folder of files named like "cat.123.jpg" / "dog.456.jpg"
     (the original Kaggle competition dump).
  2. Per-class subfolders already named cat(s)/dog(s) with any case
     (e.g. Microsoft's "PetImages/Cat", "PetImages/Dog").

Usage:
    python scripts/organize_dataset.py --source path/to/extracted/train --dest backend/data/raw
    python scripts/organize_dataset.py --source path/to/extracted/train --dest backend/data/raw --limit 1500
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CLASS_ALIASES = {"cat": "cat", "cats": "cat", "dog": "dog", "dogs": "dog"}


def find_class_subfolders(source: Path) -> dict[str, Path]:
    found = {}
    for child in source.iterdir():
        if child.is_dir() and child.name.lower() in CLASS_ALIASES:
            found[CLASS_ALIASES[child.name.lower()]] = child
    return found


def collect_from_subfolders(class_dirs: dict[str, Path], limit: int | None) -> dict[str, list[Path]]:
    result = {}
    for class_name, class_dir in class_dirs.items():
        images = sorted(p for p in class_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
        result[class_name] = images[:limit] if limit else images
    return result


def collect_from_flat_folder(source: Path, limit: int | None) -> dict[str, list[Path]]:
    result: dict[str, list[Path]] = {"cat": [], "dog": []}
    for path in sorted(source.iterdir()):
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        prefix = path.name.split(".")[0].lower()
        if prefix in CLASS_ALIASES:
            result[CLASS_ALIASES[prefix]].append(path)
    if limit:
        result = {k: v[:limit] for k, v in result.items()}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Extracted Kaggle dataset folder")
    parser.add_argument("--dest", type=Path, required=True, help="Output folder, e.g. backend/data/raw")
    parser.add_argument("--limit", type=int, default=None, help="Max images per class (for a quick trial run)")
    parser.add_argument("--move", action="store_true", help="Move files instead of copying them")
    args = parser.parse_args()

    if not args.source.is_dir():
        raise SystemExit(f"Source folder not found: {args.source}")

    class_subfolders = find_class_subfolders(args.source)
    images_by_class = (
        collect_from_subfolders(class_subfolders, args.limit)
        if class_subfolders
        else collect_from_flat_folder(args.source, args.limit)
    )

    for class_name in ("cat", "dog"):
        images = images_by_class.get(class_name, [])
        if not images:
            print(f"Warning: found 0 images for class '{class_name}'.")
            continue
        out_dir = args.dest / class_name
        out_dir.mkdir(parents=True, exist_ok=True)
        transfer = shutil.move if args.move else shutil.copy2
        for image_path in images:
            transfer(str(image_path), str(out_dir / image_path.name))
        print(f"{class_name}: {len(images)} images -> {out_dir}")


if __name__ == "__main__":
    main()
