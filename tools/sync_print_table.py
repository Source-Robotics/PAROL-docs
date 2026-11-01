#!/usr/bin/env python3
"""Show the robot repository's print table on the Printing page exactly as the owner made it.

    python tools/sync_print_table.py [--repo PATH] [--check]

Renders `Print table/Print_table.pdf` from a clone of PAROL6-Desktop-robot-arm (--repo, else $PAROL6_DIR, else a
sibling folder of this repository or ../../projects) into docs/assets/print_table.webp: the sheet as the owner
exported it from PR_EXCEL.xlsx, with its coloured headers, cropped to the table, about 2200 px wide.
docs/build/printing.md shows the image and links the PDF and the Excel file. Needs PyMuPDF and Pillow
(`pip install pymupdf pillow`); --check exits 1 when the image is missing or older than the PDF's last commit.
"""
from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "print_table.webp"
PDF = Path("Print table") / "Print_table.pdf"
WIDTH = 2200          # px of the cropped table; pages show it at about 1000 px and zoom on click
MARGIN = 24           # px of white kept around the table


def find_repo(arg: str | None) -> Path:
    for c in (arg, os.environ.get("PAROL6_DIR"), ROOT.parent / "PAROL6-Desktop-robot-arm",
              ROOT.parent.parent / "projects" / "PAROL6-Desktop-robot-arm"):
        if c and (Path(c) / PDF).exists():
            return Path(c)
    sys.exit("sync_print_table: no clone of PAROL6-Desktop-robot-arm with Print table/Print_table.pdf; pass --repo")


def render(pdf: Path) -> bytes:
    import fitz  # PyMuPDF
    from PIL import Image, ImageChops

    page = fitz.open(pdf)[0]
    zoom = 4.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    # crop to the ink: everything that is not white
    bg = Image.new("RGB", img.size, (255, 255, 255))
    box = ImageChops.difference(img, bg).convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
    if box:
        m = MARGIN * zoom / 2
        box = (max(0, box[0] - m), max(0, box[1] - m), min(img.width, box[2] + m), min(img.height, box[3] + m))
        img = img.crop(tuple(int(v) for v in box))
    if img.width > WIDTH:
        img = img.resize((WIDTH, round(img.height * WIDTH / img.width)), Image.LANCZOS)
    out = io.BytesIO()
    img.save(out, "WEBP", quality=90, method=6)
    return out.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    repo = find_repo(args.repo)
    pdf = repo / PDF
    if args.check:
        if not OUT.exists():
            print(f"{OUT.relative_to(ROOT)} is missing: run python tools/sync_print_table.py")
            return 1
        ts = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%ct", "--", str(PDF)],
                            capture_output=True, text=True).stdout.strip()
        if ts and OUT.stat().st_mtime < int(ts):
            print("the print table PDF changed after the image was made: run python tools/sync_print_table.py")
            return 1
        print("print table image is up to date")
        return 0
    data = render(pdf)
    OUT.write_bytes(data)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(data) // 1024} KB) from {pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
