import os
import glob as glob_mod
from pathlib import Path


def find_pdfs(path: str) -> list[Path]:
    """Find PDF files from a path, directory, or glob pattern."""
    p = Path(path)

    if p.is_file():
        if p.suffix.lower() == ".pdf":
            return [p.resolve()]
        return []

    if p.is_dir():
        return sorted(p.rglob("*.pdf"))

    # Treat as glob pattern
    matches = glob_mod.glob(path, recursive=True)
    return sorted(Path(m).resolve() for m in matches if Path(m).suffix.lower() == ".pdf")


def output_path(pdf_path: Path, output_dir: Path | None, fmt: str) -> Path:
    """Determine the output file path for a given PDF."""
    if output_dir:
        base = output_dir
    else:
        base = Path("output") / pdf_path.stem

    base.mkdir(parents=True, exist_ok=True)
    return base / f"{pdf_path.stem}.{fmt}"


def images_dir(pdf_path: Path, output_dir: Path | None) -> Path:
    """Determine the images output directory."""
    if output_dir:
        base = output_dir
    else:
        base = Path("output") / pdf_path.stem
    img_dir = base / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    return img_dir
