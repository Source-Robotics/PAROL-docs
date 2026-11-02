"""Write the known issues of known_issues.yml into the pages.

Two placeholders, each replaced when the site is built:

    <!-- known-issues -->              every issue: the open ones in a table per component, then the fixed ones
    <!-- known-issues: COMPONENT -->   the open issues of one component (a key under components:)

Each issue links to the page that describes it; the link is made relative to the page the table lands on, so MkDocs
checks it like any other link. A malformed issue, an unknown component, a repeated id or a page that does not exist
stops the build. Registered in mkdocs.yml under `hooks:`.
"""
from __future__ import annotations

import datetime
import posixpath
import re
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError

ALL_RE = re.compile(r"<!--\s*known-issues\s*-->")
ONE_RE = re.compile(r"<!--\s*known-issues:\s*([A-Za-z0-9_-]+)\s*-->")
REQUIRED = ("id", "component", "summary", "workaround", "page", "title", "status", "since")

_data: dict = {}


def load(path, docs_dir) -> dict:
    """known_issues.yml, checked against the docs in docs_dir. Raises PluginError naming what is wrong."""
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PluginError(f"known_issues.yml: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("components"), dict):
        raise PluginError("known_issues.yml: no components")
    for key, comp in data["components"].items():
        if not (comp or {}).get("name") or not (comp or {}).get("version"):
            raise PluginError(f"known_issues.yml: component {key!r} lacks a name or a version")
    issues = data.get("issues") or []
    seen = set()
    for issue in issues:
        missing = [f for f in REQUIRED if not issue.get(f)]
        label = issue.get("id", "an issue")
        if missing:
            raise PluginError(f"known_issues.yml: {label} lacks {', '.join(missing)}")
        if not re.fullmatch(r"KI-\d+", str(issue["id"])):
            raise PluginError(f"known_issues.yml: id {issue['id']!r} is not KI-<number>")
        if issue["id"] in seen:
            raise PluginError(f"known_issues.yml: {issue['id']} is there twice")
        seen.add(issue["id"])
        if issue["component"] not in data["components"]:
            raise PluginError(f"known_issues.yml: {label} names component {issue['component']!r}, which is not under components:")
        if issue["status"] not in ("open", "fixed"):
            raise PluginError(f"known_issues.yml: {label} status {issue['status']!r} is not open or fixed")
        if issue["status"] == "fixed" and not issue.get("fixed_in"):
            raise PluginError(f"known_issues.yml: {label} is fixed but has no fixed_in")
        if not isinstance(issue["since"], datetime.date):
            raise PluginError(f"known_issues.yml: {label} since {issue['since']!r} is not a date (YYYY-MM-DD)")
        if not (Path(docs_dir) / str(issue["page"]).split("#")[0]).is_file():
            raise PluginError(f"known_issues.yml: {label} page {issue['page']!r} is not a page under docs/")
    data["issues"] = issues
    return data


def link(issue: dict, here: str) -> str:
    """The issue's page, relative to the page `here` (a path under docs/)."""
    target, _, anchor = str(issue["page"]).partition("#")
    rel = posixpath.relpath(target, posixpath.dirname(here) or ".")
    return f"[{issue['title']}]({rel}{'#' + anchor if anchor else ''})"


def oneline(text) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def table(issues: list[dict], here: str, fixed: bool = False) -> str:
    head = "| | What happens | What to do | More |\n|---|---|---|---|\n" if not fixed else \
        "| | What happened | Fixed in | More |\n|---|---|---|---|\n"
    rows = [f"| {i['id']} | {oneline(i['summary'])} | {oneline(i['fixed_in'] if fixed else i['workaround'])} | "
            f"{link(i, here)} |" for i in issues]
    return head + "\n".join(rows)


def by_number(issue: dict) -> int:
    return int(str(issue["id"]).split("-")[1])


def component_block(key: str, data: dict, here: str, heading: bool) -> str:
    comp = data["components"][key]
    issues = sorted((i for i in data["issues"] if i["component"] == key and i["status"] == "open"), key=by_number)
    text = f"### {comp['name']}\n\n" if heading else ""
    text += f"Seen in: {comp['version']}.\n\n"
    return text + (table(issues, here) if issues else "No open issues.")


def all_issues(data: dict, here: str) -> str:
    parts = [component_block(k, data, here, True) for k in data["components"]
             if any(i["component"] == k and i["status"] == "open" for i in data["issues"])]
    fixed = sorted((i for i in data["issues"] if i["status"] == "fixed"), key=by_number)
    if fixed:
        parts.append("### Fixed\n\n" + table(fixed, here, fixed=True))
    return "\n\n".join(parts) if parts else "No known issues."


def on_config(config):
    global _data
    root = Path(config.config_file_path).parent
    _data = load(root / "known_issues.yml", config.docs_dir)
    return config


def on_page_markdown(markdown, page, config, files):
    here = page.file.src_uri

    def one(m):
        if m.group(1) not in _data["components"]:
            raise PluginError(f"{here}: <!-- known-issues: {m.group(1)} --> names no component of known_issues.yml")
        return component_block(m.group(1), _data, here, False)
    markdown = ONE_RE.sub(one, markdown)
    return ALL_RE.sub(lambda m: all_issues(_data, here), markdown)
