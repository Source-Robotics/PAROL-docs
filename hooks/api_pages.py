"""Build the Python API reference from the facts tools/sync_api.py read from the API's source at its release tag
(docs/includes/generated/api_facts.json), and the compatibility table from compatibility.yml.

Placeholders, each replaced when the site is built:

    <!-- api: NAME -->              one public method of RobotClient: heading, signature, docstring (Google style
                                    rendered as paragraphs, an argument table, an example block)
    <!-- api-tool: KIND.NAME -->    one method of a tool object (KIND electric or pneumatic)
    <!-- api-method-index -->       every method with its category and a link to the page that documents it
    <!-- api-tools-table -->        the registered tools and their variants
    <!-- api-errors-table -->       the error codes with their catalog text
    <!-- api-env-table -->          the environment variables with their defaults
    <!-- api-cli-table -->          the controller's command line options
    <!-- api-status-fields -->      the fields of the status buffer
    <!-- api-profiles -->           the motion profile names
    <!-- api-version -->            the API version the facts come from (inline)
    <!-- api-python -->             the Python version the package requires (inline)
    <!-- compatibility-table -->    the rows of compatibility.yml

A placeholder naming a method the API does not have stops the build. tools/test_tools.py checks that every public
method appears on exactly one page. Registered in mkdocs.yml under `hooks:`.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError

API_RE = re.compile(r"<!--\s*api:\s*([A-Za-z_][A-Za-z0-9_]*)\s*-->")
TOOL_RE = re.compile(r"<!--\s*api-tool:\s*(electric|pneumatic)\.([A-Za-z_][A-Za-z0-9_]*)\s*-->")
SIMPLE = {
    "api-method-index": "method_index",
    "api-tools-table": "tools_table",
    "api-errors-table": "errors_table",
    "api-env-table": "env_table",
    "api-cli-table": "cli_table",
    "api-status-fields": "status_fields",
    "api-profiles": "profiles",
    "api-version": "version",
    "api-python": "python_requires",
    "compatibility-table": "compat_table",
}
SIMPLE_RE = re.compile(r"<!--\s*(" + "|".join(SIMPLE) + r")\s*-->")
SECTION_RE = re.compile(r"^(Args|Arguments|Returns|Raises|Example|Examples|Usage|Note|Warning|Category):\s*(.*)$")

_facts: dict = {}
_methods: dict[str, dict] = {}
_pages: dict[str, str] = {}     # method name -> page src path (where its marker is)
_compat: dict = {}


def esc(text) -> str:
    return str(text).replace("|", "\\|")


def load(docs_dir: Path) -> None:
    global _facts, _methods, _pages, _compat
    path = docs_dir / "includes" / "generated" / "api_facts.json"
    try:
        _facts = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PluginError(f"api pages: {path.name}: {exc} (run python tools/sync_api.py)") from exc
    _methods = {m["name"]: m for m in _facts["methods"]}
    _pages = {}
    for p in sorted((docs_dir / "reference" / "python").glob("*.md")):
        for m in API_RE.finditer(p.read_text(encoding="utf-8")):
            _pages[m.group(1)] = p.relative_to(docs_dir).as_posix()
    try:
        _compat = yaml.safe_load((docs_dir.parent / "compatibility.yml").read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise PluginError(f"compatibility.yml: {exc}") from exc


# ---------------------------------------------------------------- rendering
def signature(name: str, params: list[dict], returns: str, prefix: str = "rbt.") -> str:
    parts = []
    for p in params:
        if p["kind"] == "separator":
            parts.append("*")
            continue
        s = p["name"]
        if p["annotation"]:
            s += f": {p['annotation']}"
        if p["default"] is not None:
            s += f" = {p['default']}" if p["annotation"] else f"={p['default']}"
        parts.append(s)
    ret = f" -> {returns}" if returns else ""
    one = f"{prefix}{name}({', '.join(parts)}){ret}"
    if len(one) <= 96:
        return one
    return f"{prefix}{name}(\n" + "".join(f"    {p},\n" for p in parts) + f"){ret}"


def inline(text: str) -> str:
    text = re.sub(r":(?:meth|attr|class|func):`~?([^`]+)`", r"`\1`", text)
    return text.replace("``", "`")


def render_doc(doc: str) -> str:
    """A Google-style docstring as Markdown: paragraphs, an argument table, returns, raises, an example block."""
    lines = doc.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    para: list[str] = []
    i = 0

    def flush():
        if para:
            out.append(inline(" ".join(s.strip() for s in para)))
            out.append("")
            para.clear()

    def block(start: int) -> tuple[list[str], int]:
        """The indented lines that belong to a section starting after line `start`."""
        body = []
        j = start
        while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith(" ")):
            body.append(lines[j])
            j += 1
        while body and body[-1].strip() == "":
            body.pop()
        return body, j

    while i < len(lines):
        line = lines[i]
        m = SECTION_RE.match(line.strip()) if not line.startswith(" ") else None
        if m:
            flush()
            kind, rest = m.group(1), m.group(2)
            body, i = block(i + 1)
            if kind == "Category":
                continue
            if kind in ("Args", "Arguments"):
                rows = []
                for b in body:
                    am = re.match(r"^\s{1,8}(\*{0,2}\w+)(?:\s*\([^)]*\))?:\s*(.*)$", b)
                    if am and not b.startswith(" " * 9):
                        rows.append([am.group(1), am.group(2)])
                    elif rows:
                        rows[-1][1] += " " + b.strip()
                if rows:
                    out.append("| Parameter | Meaning |")
                    out.append("|---|---|")
                    for n, d in rows:
                        out.append(f"| `{n}` | {esc(inline(d))} |")
                    out.append("")
            elif kind == "Returns":
                text = " ".join([rest] + [b.strip() for b in body]).strip()
                out.append(f"**Returns:** {inline(text)}")
                out.append("")
            elif kind == "Raises":
                items = []
                for b in body:
                    rm = re.match(r"^\s{1,8}(\w+):\s*(.*)$", b)
                    if rm and not b.startswith(" " * 9):
                        items.append([rm.group(1), rm.group(2)])
                    elif items:
                        items[-1][1] += " " + b.strip()
                if items:
                    out.append("**Raises:**")
                    out.append("")
                    for n, d in items:
                        out.append(f"- `{n}`: {inline(d)}")
                    out.append("")
            elif kind in ("Example", "Examples", "Usage"):
                code = [rest] if rest else []
                indent = min((len(b) - len(b.lstrip()) for b in body if b.strip()), default=0)
                code += [b[indent:] for b in body]
                out.append("```python")
                out.extend(code)
                out.append("```")
                out.append("")
            else:  # Note, Warning
                text = " ".join([rest] + [b.strip() for b in body]).strip()
                out.append(f'!!! {"warning" if kind == "Warning" else "note"}')
                out.append(f"    {inline(text)}")
                out.append("")
            continue
        if line.strip() == "":
            flush()
        else:
            para.append(line)
        i += 1
    flush()
    return "\n".join(out).rstrip() + "\n"


def method_block(name: str) -> str:
    m = _methods.get(name)
    if m is None:
        raise PluginError(f"api: no public method {name!r} in RobotClient (api_facts.json); run tools/sync_api.py or fix the marker")
    sig = signature(name, m["params"], m["returns"]) if not m["property"] else f"rbt.{name}"
    head = (f"### `{name}`" + (" (async client only)" if m.get("async_only") else "") + (" (property)" if m["property"] else "")
            + f" {{ #{name} }}")
    body = render_doc(m["doc"]) if m["doc"] else "*No docstring.*\n"
    return f"{head}\n\n```python\n{sig}\n```\n\n{body}"


def tool_block(kind: str, name: str) -> str:
    ms = {t["name"]: t for t in _facts["tools"][kind]}
    m = ms.get(name)
    if m is None:
        raise PluginError(f"api-tool: no method {name!r} on the {kind} gripper tool (api_facts.json)")
    sig = signature(name, m["params"], m["returns"], prefix="rbt.tool.")
    body = render_doc(m["doc"]) if m["doc"] else ""
    return f"### `tool.{name}` ({kind}) {{ #{kind}-{name} }}\n\n```python\n{sig}\n```\n\n{body}"


def method_index() -> str:
    rows = ["| Method | Category | Documented on |", "|---|---|---|"]
    for m in sorted(_facts["methods"], key=lambda x: (x["category"], x["name"])):
        page = _pages.get(m["name"])
        link = f"[{Path(page).stem}]({Path(page).name}#{m['name']})" if page else "—"
        rows.append(f"| `{m['name']}` | {m['category']} | {link} |")
    return "\n".join(rows)


def tools_table() -> str:
    rows = ["| Key | Tool | Variants (default first) |", "|---|---|---|"]
    for t in _facts["registered_tools"]:
        variants = list(t["variants"])
        if t["default_variant"] in variants:
            variants.remove(t["default_variant"])
            variants.insert(0, t["default_variant"])
        rows.append(f"| `{t['key']}` | {esc(t['description'])} | {', '.join(f'`{v}`' for v in variants) or '—'} |")
    return "\n".join(rows)


def errors_table() -> str:
    rows = ["| Code | Number | Title | Cause | Effect | Remedy |", "|---|---|---|---|---|---|"]
    for e in _facts["errors"]:
        num = "shared" if e["code"] is None else str(e["code"])
        rows.append(f"| `{e['name']}` | {num} | {esc(e['title'])} | {esc(e['cause'])} | {esc(e['effect'])} | {esc(e['remedy'])} |")
    return "\n".join(rows)


def env_table() -> str:
    rows = ["| Variable | Default |", "|---|---|"]
    for v in _facts["env"]:
        rows.append(f"| `{v['name']}` | `{v['default']}` |" if v["default"] != "" else f"| `{v['name']}` | — |")
    return "\n".join(rows)


def cli_table() -> str:
    rows = ["| Option | Default | Meaning |", "|---|---|---|"]
    for o in _facts["cli"]:
        flags = ", ".join(f"`{f}`" for f in o["flags"])
        default = f"`{o['default']}`" if o["default"] else ("flag" if o["action"] in ("store_true", "count") else "—")
        meaning = esc(o["help"]) + (f" (one of {', '.join(f'`{c}`' for c in o['choices'])})" if o["choices"] else "")
        rows.append(f"| {flags} | {default} | {meaning} |")
    return "\n".join(rows)


def status_fields() -> str:
    rows = ["| Field | Type |", "|---|---|"]
    for f in _facts["status_fields"]:
        rows.append(f"| `{f['name']}` | `{esc(f['type'])}` |")
    return "\n".join(rows)


def profiles() -> str:
    return ", ".join(f"`{p}`" for p in _facts["profiles"])


def version() -> str:
    return _facts["generated_from"]["tag"]


def python_requires() -> str:
    return _facts.get("python_requires") or "3.11 or newer"


def compat_table() -> str:
    cols = _compat.get("columns") or []
    rows = ["| " + " | ".join(c["title"] for c in cols) + " |", "|" + "---|" * len(cols)]
    for r in _compat.get("rows") or []:
        rows.append("| " + " | ".join(esc(r.get(c["key"], "")) for c in cols) + " |")
    return "\n".join(rows)


# ---------------------------------------------------------------- the hook
def on_config(config):
    load(Path(config.docs_dir))
    return config


def on_page_markdown(markdown, page, config, files):
    markdown = API_RE.sub(lambda m: method_block(m.group(1)), markdown)
    markdown = TOOL_RE.sub(lambda m: tool_block(m.group(1), m.group(2)), markdown)
    return SIMPLE_RE.sub(lambda m: globals()[SIMPLE[m.group(1)]](), markdown)
