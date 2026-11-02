"""Captions under the pictures: every standalone picture becomes a numbered figure, its description the caption.

A picture on a line of its own, with a blank line (or the start of its block) before and after it, is wrapped in the
manuals' figure form (the same as Source-Robotics/par6's devlab "Figure with a numbered caption"):

    <figure markdown="span">
      ![alt](picture.webp#only-light){ width="900" }
      ![alt](picture_dark.webp#only-dark){ width="900" }
      <figcaption>Figure 3.2: alt.</figcaption>
    </figure>

A light and a dark version of one picture (two lines, #only-light and #only-dark) are one figure. The caption is the
picture's alt text, so a picture is described once. Numbering: per chapter in reading order (nav order) for pages
under a numbered chapter folder or file (03-technical-data/..., 09-transport.md, board/05-...: "Figure 3.2"),
per page elsewhere ("Figure 2"). Pictures with the class .hero, pictures inside a paragraph of text and pictures
without alt text are left as they are. Registered in mkdocs.yml under `hooks:`, after llms.py, so the Markdown twins
keep plain pictures.
"""
from __future__ import annotations

import html
import re
from collections import defaultdict
from pathlib import Path

IMG = re.compile(r"^(?P<ind>[ \t]*)!\[(?P<alt>[^\]]+)\]\((?P<src>[^)\s]+)\)(?P<attr>\{[^}]*\})?[ \t]*$")
NUMBERED = re.compile(r"^(\d{2})-")
_start: dict[str, int] = {}


def chapter(uri: str) -> tuple[str, str]:
    """(counter key, label prefix): a numbered chapter counts across its pages, any other page on its own."""
    parts = uri.replace("\\", "/").split("/")
    for i, part in enumerate(parts):
        m = NUMBERED.match(part)
        if m:
            return "/".join(parts[:i + 1]), f"{int(m.group(1))}."
    return uri, ""


def figure_runs(lines: list[str]):
    """(first, last) line index of each run of one or two standalone pictures that makes one figure."""
    runs, i = [], 0
    while i < len(lines):
        m = IMG.match(lines[i])
        if not m or ".hero" in (m["attr"] or "") or (i > 0 and lines[i - 1].strip()
                                                         and not lines[i - 1].lstrip().startswith(("===", "!!!", "???"))):
            i += 1
            continue
        j = i
        if j + 1 < len(lines):
            n = IMG.match(lines[j + 1])
            if n and n["ind"] == m["ind"] and ("#only-light" in m["src"] or "#only-dark" in m["src"]):
                j += 1
        if j + 1 < len(lines) and lines[j + 1].strip():
            i = j + 1
            continue
        runs.append((i, j))
        i = j + 1
    return runs


def wrap(lines: list[str], first: int, last: int, label: str) -> list[str]:
    m = IMG.match(lines[first])
    ind = m["ind"]
    alt = m["alt"].strip()
    caption = alt if alt.endswith((".", "!", "?")) else alt + "."
    out = [f'{ind}<figure markdown="span">']
    out += [f"{ind}  {lines[k].strip()}" for k in range(first, last + 1)]
    out += [f"{ind}  <figcaption>Figure {label}: {html.escape(caption, quote=False)}</figcaption>", f"{ind}</figure>"]
    return out


def transform(markdown: str, start: int, prefix: str) -> tuple[str, int]:
    lines = markdown.split("\n")
    runs = figure_runs(lines)
    n = start
    labels = {}
    for first, last in runs:
        n += 1
        labels[first] = f"{prefix}{n}"
    for first, last in reversed(runs):
        lines[first:last + 1] = wrap(lines, first, last, labels[first])
    return "\n".join(lines), len(runs)


def on_nav(nav, config, files):
    """Number in reading order: count each page's figures in nav order, per chapter."""
    _start.clear()
    count = defaultdict(int)
    for page in nav.pages:
        uri = page.file.src_uri
        key, _ = chapter(uri)
        try:
            text = Path(page.file.abs_src_path).read_text(encoding="utf-8").replace("\r\n", "\n")
        except OSError:
            continue
        _start[uri] = count[key]
        count[key] += len(figure_runs(text.split("\n")))
    return nav


def on_page_markdown(markdown, page, config, files):
    uri = page.file.src_uri
    _, prefix = chapter(uri)
    text, _ = transform(markdown.replace("\r\n", "\n"), _start.get(uri, 0), prefix)
    return text
