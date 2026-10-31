"""Regression checks for release-pinned exports, issue links and runnable Python syntax."""
import ast
import html
import importlib.util
import os
import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from jinja2 import DictLoader, Environment

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("llms_test", ROOT / "hooks/llms.py")
llms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llms)


def config(site="https://docs.example/product/", version="107"):
    return SimpleNamespace(site_url=site, docs_dir=str(ROOT / "docs"),
                           extra={"docs_version": version}, repo_url="https://github.com/example/docs")


class SiteFeatures(unittest.TestCase):
    def test_export_links_pin_the_release_once(self):
        with patch.dict(os.environ, {"MIKE_DOCS_VERSION": ""}):
            self.assertEqual(llms.base_url(config()), "https://docs.example/product/107/")
            self.assertEqual(llms.base_url(config("https://docs.example/product/107")),
                             "https://docs.example/product/107/")
        with patch.dict(os.environ, {"MIKE_DOCS_VERSION": "106"}):
            self.assertEqual(llms.base_url(config()), "https://docs.example/product/106/")

    def test_webp_and_downloads_resolve_from_the_source_directory(self):
        cfg = config()
        page = SimpleNamespace(file=SimpleNamespace(src_uri="reference/can/example.md"),
                               title="Example", url="reference/can/example/")
        with patch.dict(os.environ, {"MIKE_DOCS_VERSION": ""}):
            llms.on_page_markdown("# Example\n\n![Chart](../../assets/force.webp)\n"
                                  "[DBC](../../assets/can/test.dbc)\n[Guide](../../quick-start.md)",
                                  page, cfg, None)
        text = llms._pages[page.file.src_uri]["markdown"]
        self.assertIn("https://docs.example/product/107/assets/force.webp", text)
        self.assertIn("https://docs.example/product/107/assets/can/test.dbc", text)
        self.assertIn("https://docs.example/product/107/quick-start/", text)
        self.assertNotIn("latest/", text)

    def test_issue_body_has_real_newlines_and_the_release(self):
        cfg = config()
        with patch.dict(os.environ, {"MIKE_DOCS_VERSION": ""}):
            llms.on_config(cfg)
        env = Environment(loader=DictLoader({
            "base.html": "{% block content %}{% endblock %}",
            "page.html": (ROOT / "overrides/main.html").read_text(encoding="utf-8")}))
        env.filters["url"] = lambda value: value
        page = SimpleNamespace(edit_url="https://github.com/example/docs/edit/main/page.md", title="A & B",
                               url="reference/example/")
        rendered = env.get_template("page.html").render(page=page, config=cfg)
        href = html.unescape(re.search(r'href="([^"]+/issues/new\?[^"]+)"', rendered).group(1))
        body = parse_qs(urlsplit(href).query)["body"][0]
        self.assertIn("https://docs.example/product/107/reference/example/", body)
        self.assertIn("\n\nDocumentation version: 107\n\nWhat is wrong:\n", body)
        self.assertNotIn("%0A", body)

    def test_python_examples_have_valid_syntax(self):
        fence = re.compile(r"^([ \t]*)```[ \t]*(?:python|py)(?:[^\n]*)\n(.*?)^\1```", re.M | re.S)
        for path in (ROOT / "docs").rglob("*.md"):
            if "includes" in path.relative_to(ROOT / "docs").parts:
                continue
            for match in fence.finditer(path.read_text(encoding="utf-8")):
                indent = match.group(1)
                code = "\n".join(line[len(indent):] if line.startswith(indent) else line
                                 for line in match.group(2).splitlines())
                with self.subTest(page=str(path.relative_to(ROOT)), line=match.start()):
                    ast.parse(code, filename=str(path))


if __name__ == "__main__":
    unittest.main()
