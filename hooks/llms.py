"""The site for readers that are programs: a Markdown twin of every page, llms.txt and llms-full.txt.

Every page is also served as Markdown at its own address followed by index.md (…/05-setup/motor-gui/index.md): the
page's source with the site's placeholders and snippets expanded, its attribute lists and comments removed and its
links made absolute. /llms.txt indexes the twins by tab, with each page's first sentence; /llms-full.txt holds
every page in one file, in the order of the navigation. The "Copy this page as Markdown" button in the page header
(docs/javascripts/copy-markdown.js) reads the twin.

The absolute links stay pinned to the release in versions.yml (or MIKE_DOCS_VERSION during publishing).
The mike plugin may already have appended that release to site_url; never append it twice. Registered last in mkdocs.yml under `hooks:`, after the hooks that write
the version box and the reference pages, so that it sees their output.
"""
from __future__ import annotations

import os
import posixpath
import re
from pathlib import Path

SNIPPET_RE = re.compile(r'^--8<--\s+"([^"]+)"\s*$', re.M)
PAGE_LINK_RE = re.compile(r"\]\((?!https?://|mailto:|#|/)([^)\s]+?\.md)(#[^)]*)?\)")
FILE_LINK_RE = re.compile(r"\]\((?!https?://|mailto:|#|/)([^)\s]+?\.(?:png|jpe?g|webp|avif|svg|gif|pdf|glb|json|ya?ml|csv|dbc))(?:#[^)]*)?\)", re.I)
ATTR_RE = re.compile(r"\{\s*[.#:][^}]*\}")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

_pages: dict[str, dict] = {}     # src_uri -> {title, url, markdown}


def base_url(config) -> str:
    site = str(config.site_url).rstrip("/") + "/"
    sub = str(os.environ.get("MIKE_DOCS_VERSION") or (config.extra or {}).get("docs_version") or "").strip("/")
    # mike already appends the version to site_url; plain mkdocs builds do not.
    if sub and not site.rstrip("/").endswith("/" + sub):
        site += sub + "/"
    return site


def on_config(config):
    _pages.clear()
    config.extra["docs_base_url"] = base_url(config)
    return config


def page_url(src: str) -> str:
    """The directory URL of a page source path: 'a/b.md' -> 'a/b/', 'a/index.md' -> 'a/', 'index.md' -> ''."""
    stem = src[:-3]
    if stem == "index":
        return ""
    if stem.endswith("/index"):
        return stem[:-6] + "/"
    return stem + "/"


def on_page_markdown(markdown, page, config, files):
    docs = Path(config.docs_dir)
    base = base_url(config)
    src_dir = posixpath.dirname(page.file.src_uri)

    def snippet(m):
        p = docs / "includes" / m.group(1)
        return p.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n") if p.exists() else ""

    def link(m):
        target = posixpath.normpath(posixpath.join(src_dir, m.group(1)))
        return f"]({base}{page_url(target)}{m.group(2) or ''})"

    def file(m):
        return f"]({base}{posixpath.normpath(posixpath.join(src_dir, m.group(1)))})"

    md = SNIPPET_RE.sub(snippet, markdown)
    md = COMMENT_RE.sub("", md)
    md = PAGE_LINK_RE.sub(link, md)
    md = FILE_LINK_RE.sub(file, md)
    md = ATTR_RE.sub("", md)
    md = re.sub(r"^---\n.*?\n---\n", "", md, count=1, flags=re.S)       # front matter
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    _pages[page.file.src_uri] = {"title": page.title or Path(page.file.src_uri).stem, "url": page.url, "markdown": md}
    return markdown


def nav_sections(config) -> list[tuple[str, list[str]]]:
    """[(tab title, [src_uri, ...]), ...] in the order of the navigation."""
    out = []

    def walk(node, acc):
        if isinstance(node, str):
            acc.append(node)
        elif isinstance(node, list):
            for n in node:
                walk(n, acc)
        elif isinstance(node, dict):
            for v in node.values():
                walk(v, acc)
    for tab in config.nav or []:
        if isinstance(tab, dict):
            for title, node in tab.items():
                acc: list[str] = []
                walk(node, acc)
                out.append((str(title), acc))
    return out


def first_sentence(md: str) -> str:
    for para in re.split(r"\n\s*\n", md):
        p = para.strip()
        if not p or p.startswith(("#", "!", "|", "<", "-", "*", "[", "```", "$$", "=", "    ")):
            continue
        p = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", p)
        p = re.sub(r"[*`_]", "", p).replace("\n", " ")
        m = re.match(r"(.{20,220}?[.!?])(\s|$)", p)
        return (m.group(1) if m else p[:220]).strip()
    return ""


def on_post_build(config):
    site = Path(config.site_dir)
    base = base_url(config)
    intro = (f"# {config.site_name}\n\n> {config.site_description}\n\n"
             "Every page of this site is also available as Markdown at its address followed by `index.md`, with its "
             "links absolute; `llms-full.txt` holds every page in one file. The version box on the landing page names "
             "the release the pages describe.\n")
    index = [intro]
    full = [intro, f"Full text of every page, in the order of the site's navigation. Source: {base}\n"]
    for tab, srcs in nav_sections(config):
        index.append(f"\n## {tab}\n")
        for src in srcs:
            p = _pages.get(src)
            if p is None:
                continue
            twin = site / p["url"] / "index.md"
            twin.parent.mkdir(parents=True, exist_ok=True)
            twin.write_text(p["markdown"], encoding="utf-8")
            sentence = first_sentence(p["markdown"])
            index.append(f"- [{p['title']}]({base}{p['url']}index.md)" + (f": {sentence}" if sentence else ""))
            full.append(f"\n---\n\n<!-- {base}{p['url']} -->\n\n{p['markdown']}")
    (site / "llms.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    (site / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")
