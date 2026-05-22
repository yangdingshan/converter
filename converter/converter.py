import base64
import re
import shutil
from pathlib import Path

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered


_converter: PdfConverter | None = None


def _get_converter() -> PdfConverter:
    global _converter
    if _converter is None:
        _converter = PdfConverter(artifact_dict=create_model_dict())
    return _converter


def _strip_markdown(text: str) -> str:
    """Convert markdown to plain text."""
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _process_images(md_text: str, img_dir: Path, mode: str) -> str:
    """Handle images: extract, embed, or remove."""
    img_dir = img_dir.resolve()

    def _replace(m: re.Match) -> str:
        alt = m.group(1)
        src = m.group(2)

        if mode == "skip":
            return ""

        if mode == "embed":
            img_path = img_dir / src if not Path(src).is_absolute() else Path(src)
            if img_path.exists():
                ext = img_path.suffix.lower()
                mime_map = {".png": "image/png", ".jpg": "image/jpeg",
                            ".jpeg": "image/jpeg", ".gif": "image/gif",
                            ".webp": "image/webp", ".bmp": "image/bmp"}
                mime = mime_map.get(ext, "image/png")
                b64 = base64.b64encode(img_path.read_bytes()).decode()
                return f"![{alt}](data:{mime};base64,{b64})"

        return m.group(0)

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _replace, md_text)


def convert(
    pdf_path: Path,
    output_dir: Path | None = None,
    fmt: str = "md",
    images: str = "extract",
    ocr: bool = False,
) -> Path:
    pdf_path = pdf_path.resolve()

    if output_dir:
        out_dir = output_dir.resolve()
    else:
        out_dir = (Path("output") / pdf_path.stem).resolve()

    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = out_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    converter = _get_converter()
    rendered = converter(str(pdf_path))
    md_text, metadata, extracted_images = text_from_rendered(rendered)

    for name, img in extracted_images.items():
        img.save(str(img_dir / name))

    if images == "skip":
        md_text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", "", md_text)
    elif images == "embed":
        md_text = _process_images(md_text, img_dir, "embed")

    if fmt == "txt":
        md_text = _strip_markdown(md_text)

    ext = fmt if fmt == "txt" else "md"
    out_path = out_dir / f"{pdf_path.stem}.{ext}"
    out_path.write_text(md_text, encoding="utf-8")

    if images == "skip" and img_dir.exists():
        shutil.rmtree(img_dir)

    return out_path


def convert_batch(
    pdf_paths: list[Path],
    output_dir: Path | None = None,
    fmt: str = "md",
    images: str = "extract",
    ocr: bool = False,
) -> list[Path]:
    results = []
    for pdf_path in pdf_paths:
        out = convert(pdf_path, output_dir, fmt, images, ocr)
        results.append(out)
    return results
