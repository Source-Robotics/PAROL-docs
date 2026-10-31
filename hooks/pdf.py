"""The PDF of the manual: prints the print-site plugin's page (every chapter in order, a cover and a table of
contents) with headless Chrome, so that the PDF looks like the site, diagrams and tables included. Chrome keeps
every picture uncompressed at full size, so the file is then shrunk with PyMuPDF: the pictures recompressed as
JPEG at print size (transparent ones on white, as on paper), the objects packed. That takes a manual from tens
of MB to a few.

Runs only when the environment variable DOCS_PDF is set: the CI sets it for the publish (the PDF lands in the
published version next to the pages), a local build sets it on demand:

    DOCS_PDF=1 mkdocs build          # Windows PowerShell: $env:DOCS_PDF = "1"; mkdocs build

The file is site/<extra.pdf.file>; the page-help line of every page links it while the hook is on. Chrome is
found through CHROME_BIN or the usual places (google-chrome on the runners). The print page is rendered in the
light scheme for paper, and the cookie banner is removed before printing.
"""
from __future__ import annotations

import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

CANDIDATES = ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium", "chrome",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
PICTURE_PX = 1600      # the long side of a picture in the PDF: about 240 dpi across a page's text width
JPEG_QUALITY = 80


def enabled() -> bool:
    return bool(os.environ.get("DOCS_PDF"))


def chrome() -> str | None:
    if os.environ.get("CHROME_BIN"):
        return os.environ["CHROME_BIN"]
    for c in CANDIDATES:
        if Path(c).exists():
            return c
        found = shutil.which(c)
        if found:
            return found
    return None


def shrink(path: Path) -> str:
    """Recompress the pictures of the PDF at path as JPEG of at most PICTURE_PX and pack its objects, in place."""
    try:
        import fitz                     # PyMuPDF
        from PIL import Image
    except ImportError:
        return "not shrunk: PyMuPDF is not installed"
    doc = fitz.open(path)
    done = set()
    for page in doc:
        for xref, smask, width, height, *_, codec in (i[:9] for i in page.get_images(full=True)):
            if xref in done:
                continue
            done.add(xref)
            small = max(width, height) <= PICTURE_PX
            if not smask and small and (codec == "DCTDecode" or len(doc.xref_stream_raw(xref)) < 40_000):
                continue                # already a JPEG of print size, or a small icon
            pix = fitz.Pixmap(doc, xref)
            if smask:
                pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
            if pix.colorspace and pix.colorspace.n not in (1, 3):
                pix = fitz.Pixmap(fitz.csRGB, pix)
            mode = {1: "L", 2: "LA", 3: "RGB", 4: "RGBA"}[pix.n]
            picture = Image.frombytes(mode, (pix.width, pix.height), pix.samples).convert("RGBA")
            paper = Image.new("RGBA", picture.size, "white")
            paper.alpha_composite(picture)
            picture = paper.convert("RGB")
            picture.thumbnail((PICTURE_PX, PICTURE_PX))
            jpeg = io.BytesIO()
            picture.save(jpeg, "JPEG", quality=JPEG_QUALITY, optimize=True)
            page.replace_image(xref, stream=jpeg.getvalue())
    packed = path.with_name(path.stem + ".packed.pdf")
    doc.save(packed, garbage=4, deflate=True, use_objstms=1)
    doc.close()
    packed.replace(path)
    return f"{len(done)} pictures checked"


def on_config(config):
    pdf = (config.extra or {}).get("pdf") or {}
    pdf["enabled"] = enabled() and bool(pdf.get("file"))
    config.extra["pdf"] = pdf
    return config


def on_post_build(config):
    pdf = config.extra.get("pdf") or {}
    if not pdf.get("enabled"):
        return
    site = Path(config.site_dir)
    page = site / "print_page" / "index.html"
    if not page.exists():
        print("pdf: no print page (is the print-site plugin enabled?)", file=sys.stderr)
        return
    exe = chrome()
    if not exe:
        print("pdf: no Chrome found; set CHROME_BIN", file=sys.stderr)
        return
    html = page.read_text(encoding="utf-8")
    html = html.replace('data-md-color-scheme="slate"', 'data-md-color-scheme="default"')
    html = html.replace("</body>", '<script>var c = document.getElementById("__consent"); if (c) c.remove();</script></body>')
    paper = page.with_name("paper.html")
    paper.write_text(html, encoding="utf-8")
    out = site / pdf["file"]
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [exe, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer", "--hide-scrollbars",
           "--run-all-compositor-stages-before-draw", "--virtual-time-budget=60000",
           f"--print-to-pdf={out}", paper.resolve().as_uri()]
    try:
        subprocess.run(cmd, check=True, timeout=600, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        paper.unlink(missing_ok=True)
    printed = out.stat().st_size // 1024
    note = shrink(out)
    print(f"pdf: {out.relative_to(site)} ({printed} KB printed, {out.stat().st_size // 1024} KB shrunk; {note})")
