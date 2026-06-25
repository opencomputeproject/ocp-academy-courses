#!/usr/bin/env python3
"""
extract_figures.py — pull figures referenced by course.json (source = "reuse")
out of the source PDFs / PPTX files into <course-folder>/figures/.

Usage:
    python extract_figures.py <course.json>

For each slide whose figure has `source: "reuse"` and an `extract_from`:
    {"source": "<absolute or course-relative path to source file>", "page": <N>}

If the source is a PDF, this script renders the page at 200dpi to PNG and writes
it to the figure.path destination. (Renders the whole page; for surgical crops,
adjust by hand in the course.json or post-edit the PNG.)

If the source is a PPTX, this exports the slide at index N (1-based) by
unzipping the pptx and grabbing the corresponding slide-rendered PNG via
LibreOffice headless export. Requires `libreoffice` or `soffice` in PATH.

For finer-grained extraction (an embedded image rather than a whole page), you
can declare `extract_from.image_index` and we'll attempt to pull image N from
the page's resource dict (PDF only).
"""

from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def need(cmd: str) -> str | None:
    return shutil.which(cmd)


def render_pdf_page(pdf_path: Path, page: int, out_png: Path, image_index: int | None = None) -> None:
    """Render a PDF page to PNG. Uses pypdfium2 if installed (fast), else pdftoppm."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    if image_index is None:
        # whole-page render
        try:
            import pypdfium2 as pdfium  # type: ignore
        except ImportError:
            pdfium = None
        if pdfium is not None:
            pdf = pdfium.PdfDocument(str(pdf_path))
            pg = pdf[page - 1]
            pil = pg.render(scale=200/72).to_pil()
            pil.save(out_png, "PNG")
            return
        if need("pdftoppm"):
            with tempfile.TemporaryDirectory() as tmp:
                subprocess.run(["pdftoppm", "-png", "-r", "200", "-f", str(page), "-l", str(page),
                                str(pdf_path), str(Path(tmp) / "p")], check=True)
                outs = sorted(Path(tmp).glob("p-*.png"))
                if not outs:
                    raise RuntimeError("pdftoppm produced no output")
                shutil.copy(outs[0], out_png)
            return
        raise RuntimeError("Need pypdfium2 (pip install pypdfium2) or pdftoppm (poppler-utils).")
    else:
        # extract embedded image N on that page
        try:
            import fitz  # type: ignore
        except ImportError:
            raise RuntimeError("Embedded image extraction needs PyMuPDF (pip install pymupdf).")
        doc = fitz.open(str(pdf_path))
        page_obj = doc[page - 1]
        images = page_obj.get_images(full=True)
        if image_index < 0 or image_index >= len(images):
            raise RuntimeError(f"image_index {image_index} out of range; page has {len(images)} images")
        xref = images[image_index][0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha >= 4:  # CMYK
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.save(str(out_png))
        doc.close()


def render_pptx_slide(pptx_path: Path, slide: int, out_png: Path) -> None:
    """Render a PPTX slide via LibreOffice headless -> per-slide PDF -> PNG."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    soffice = need("libreoffice") or need("soffice")
    if not soffice:
        raise RuntimeError("PPTX extraction requires LibreOffice (`brew install libreoffice` on macOS).")
    with tempfile.TemporaryDirectory() as tmp:
        # Convert pptx -> pdf
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, str(pptx_path)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pdfs = list(Path(tmp).glob("*.pdf"))
        if not pdfs:
            raise RuntimeError("LibreOffice produced no PDF")
        render_pdf_page(pdfs[0], slide, out_png)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("course_json", type=Path)
    args = p.parse_args()
    course = json.loads(args.course_json.read_text())
    base = args.course_json.resolve().parent

    n_done = 0
    n_skip = 0
    for mod in course["modules"]:
        for slide in mod["slides"]:
            fig = slide.get("figure")
            if not fig or fig.get("source") != "reuse":
                continue
            ext = fig.get("extract_from") or {}
            src = ext.get("source")
            page = ext.get("page")
            if not src or not page:
                print(f"  SKIP figure {fig.get('path','?')}: no extract_from.source/page")
                continue
            src_path = Path(src)
            if not src_path.is_absolute():
                src_path = (base / src_path).resolve()
            out_png = base / fig["path"]
            if out_png.exists():
                n_skip += 1
                continue
            try:
                if src_path.suffix.lower() == ".pdf":
                    render_pdf_page(src_path, int(page), out_png, ext.get("image_index"))
                elif src_path.suffix.lower() in (".pptx", ".ppt"):
                    render_pptx_slide(src_path, int(page), out_png)
                else:
                    print(f"  SKIP {fig['path']}: unsupported source type {src_path.suffix}")
                    continue
                n_done += 1
                print(f"  OK {out_png.relative_to(base)}")
            except Exception as e:
                print(f"  FAIL {fig.get('path','?')}: {e}", file=sys.stderr)

    print(f"\nextracted: {n_done}; already present: {n_skip}")


if __name__ == "__main__":
    main()
