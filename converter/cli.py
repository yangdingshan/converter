import sys
from pathlib import Path

import click

from .converter import convert, convert_batch
from .utils import find_pdfs


@click.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), default=None,
              help="Output directory or file path.")
@click.option("-f", "--format", "fmt", type=click.Choice(["md", "txt"]), default="md",
              help="Output format: markdown (md) or plain text (txt).")
@click.option("--no-images", is_flag=True, default=False,
              help="Skip image extraction entirely.")
@click.option("--embed-images", is_flag=True, default=False,
              help="Embed images as Base64 instead of extracting to folder.")
@click.option("--ocr", is_flag=True, default=False,
              help="Force OCR mode for scanned PDFs.")
def main(source: str, output: str | None, fmt: str,
         no_images: bool, embed_images: bool, ocr: bool) -> None:

    pdfs = find_pdfs(source)
    if not pdfs:
        click.secho(f"No PDF files found at: {source}", fg="red", err=True)
        sys.exit(1)

    images = "skip" if no_images else ("embed" if embed_images else "extract")

    click.secho(f"Found {len(pdfs)} PDF(s) to convert.\n", fg="cyan")

    out_dir = Path(output) if output else None

    if len(pdfs) == 1:
        out = convert(pdfs[0], out_dir, fmt, images, ocr)
        click.secho(f"Done → {out}", fg="green")
    else:
        results = convert_batch(pdfs, out_dir, fmt, images, ocr)
        for r in results:
            click.secho(f"Done → {r}", fg="green")

    click.secho(f"\nConverted {len(pdfs)} file(s).", fg="green")
