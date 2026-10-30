"""The PDF of the manual: prints the print-site plugin's page (every chapter in order, a cover and a table of
contents) with headless Chrome, so that the PDF looks like the site, diagrams and tables included.

Runs only when the environment variable DOCS_PDF is set: the CI sets it for the publish (the PDF lands in the
published version next to the pages), a local build sets it on demand:

    DOCS_PDF=1 mkdocs build          # Windows PowerShell: $env:DOCS_PDF = "1"; mkdocs build

The file is site/<extra.pdf.file>; the page-help line of every page links it while the hook is on. Chrome is
found through CHROME_BIN or the usual places (google-chrome on the runners). The print page is rendered in the
light scheme for paper, and the cookie banner is removed before printing.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

CANDIDATES = ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium", "chrome",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]


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
    print(f"pdf: {out.relative_to(site)} ({out.stat().st_size // 1024} KB)")
