#!/usr/bin/env python3
"""Read the facts of the PAROL6 Python API from its source at the release tag named in versions.yml
(software.python_api.tag), and write them to docs/includes/generated/ for hooks/api_pages.py:

    api_facts.json          the public methods of RobotClient (signature, docstring, category), the tool methods,
                            the registered tools and their variants, the error codes with their catalog text, the
                            environment variables with their defaults, the controller's command line options, the
                            status fields, the motion profiles, the command and query type names, the protocol
                            version, the Python version the package needs
    api_release_notes.md    the bodies of the GitHub releases of the API, newest first (needs the network)

Nothing is read from a working tree: the source comes from `git show TAG:path` of a clone of the API repository
with its tags, found next to this repository (../PAROL6-python-API), under ../../projects/, or named by --api PATH
or the API_DIR environment variable.

    python tools/sync_api.py                 write both files
    python tools/sync_api.py --check         exit 1 if api_facts.json is out of date (the release notes are not compared)
    python tools/sync_api.py --no-network    keep the release notes file that is there
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "includes" / "generated"
REPO_NAME = "PAROL6-python-API"
SYNC_CLIENT = "parol6/client/sync_client.py"
ASYNC_CLIENT = "parol6/client/async_client.py"
ROBOT = "parol6/robot.py"
TOOLS = "parol6/tools.py"
ERROR_CODES = "parol6/utils/error_codes.py"
ERROR_CATALOG = "parol6/utils/error_catalog.py"
CONFIG = "parol6/config.py"
WIRE = "parol6/protocol/wire.py"
CLI = "parol6/server/cli.py"
PYPROJECT = "pyproject.toml"


# ---------------------------------------------------------------- the repository
def find_api(arg: str | None) -> Path:
    candidates = [arg, os.environ.get("API_DIR"), ROOT.parent / REPO_NAME, ROOT.parent.parent / "projects" / REPO_NAME]
    for c in candidates:
        if c and (Path(c) / "parol6").is_dir():
            return Path(c)
    raise SystemExit(f"no clone of {REPO_NAME} found: pass --api PATH or set API_DIR")


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def show(repo: Path, tag: str, path: str) -> str:
    return git(repo, "show", f"{tag}:{path}")


# ---------------------------------------------------------------- the client methods
def is_overload(f: ast.AST) -> bool:
    return any(isinstance(d, ast.Name) and d.id == "overload" for d in f.decorator_list)


def is_property(f: ast.AST) -> bool:
    return any(isinstance(d, ast.Name) and d.id == "property" for d in f.decorator_list)


def is_setter(f: ast.AST) -> bool:
    return any(isinstance(d, ast.Attribute) and d.attr == "setter" for d in f.decorator_list)


def params_of(f: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict]:
    """The parameters of a method, self dropped, in signature order, with their kind."""
    a = f.args
    out = []
    pos = [*a.posonlyargs, *a.args]
    defaults = [None] * (len(pos) - len(a.defaults)) + list(a.defaults)
    for i, (p, d) in enumerate(zip(pos, defaults)):
        if i == 0 and p.arg in ("self", "cls"):
            continue
        out.append({"name": p.arg, "annotation": ast.unparse(p.annotation) if p.annotation else "",
                    "default": ast.unparse(d) if d is not None else None,
                    "kind": "positional-only" if p in a.posonlyargs else "positional"})
    if a.vararg:
        out.append({"name": "*" + a.vararg.arg, "annotation": ast.unparse(a.vararg.annotation) if a.vararg.annotation else "",
                    "default": None, "kind": "var-positional"})
    elif a.kwonlyargs:
        out.append({"name": "*", "annotation": "", "default": None, "kind": "separator"})
    for p, d in zip(a.kwonlyargs, a.kw_defaults):
        out.append({"name": p.arg, "annotation": ast.unparse(p.annotation) if p.annotation else "",
                    "default": ast.unparse(d) if d is not None else None, "kind": "keyword-only"})
    if a.kwarg:
        out.append({"name": "**" + a.kwarg.arg, "annotation": ast.unparse(a.kwarg.annotation) if a.kwarg.annotation else "",
                    "default": None, "kind": "var-keyword"})
    return out


def class_methods(src: str, cls_name: str) -> dict[str, dict]:
    tree = ast.parse(src)
    cls = next((n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == cls_name), None)
    if cls is None:
        raise SystemExit(f"class {cls_name} not found")
    out: dict[str, dict] = {}
    for f in cls.body:
        if not isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)) or f.name.startswith("_"):
            continue
        if is_overload(f) or is_setter(f):
            continue
        out[f.name] = {"name": f.name, "params": params_of(f), "returns": ast.unparse(f.returns) if f.returns else "",
                       "doc": ast.get_docstring(f) or "", "property": is_property(f),
                       "async": isinstance(f, ast.AsyncFunctionDef)}
    return out


CATEGORY_RE = re.compile(r"^Category:\s*(.+?)\s*$", re.M)


def client_methods(sync_src: str, async_src: str) -> list[dict]:
    """RobotClient's public methods: the sync signature (what a script calls), the richer of the two docstrings."""
    sync = class_methods(sync_src, "RobotClient")
    asy = class_methods(async_src, "AsyncRobotClient")
    out = []
    for name, m in sync.items():
        doc = m["doc"]
        other = asy.get(name, {}).get("doc", "")
        if "Category:" not in doc and other:
            doc = other
        cat = CATEGORY_RE.search(doc)
        out.append({"name": name, "params": m["params"], "returns": m["returns"], "doc": doc,
                    "category": cat.group(1) if cat else ("Property" if m["property"] else "Other"),
                    "property": m["property"], "async_only": False})
    for name, m in asy.items():
        if name not in sync and not m["property"]:
            cat = CATEGORY_RE.search(m["doc"])
            out.append({"name": name, "params": m["params"], "returns": m["returns"], "doc": m["doc"],
                        "category": cat.group(1) if cat else "Other", "property": False, "async_only": True})
    return out


# ---------------------------------------------------------------- the tools
def tool_methods(robot_src: str) -> dict[str, list[dict]]:
    out = {}
    for key, cls in (("electric", "_ElectricGripperImpl"), ("pneumatic", "_PneumaticGripperImpl")):
        ms = class_methods(robot_src, cls)
        out[key] = [{"name": n, "params": m["params"], "returns": m["returns"], "doc": m["doc"]}
                    for n, m in ms.items() if not m["property"] and n not in ("action_r",)]
    return out


def registered_tools(tools_src: str) -> list[dict]:
    blocks = re.split(r"^register_tool\(", tools_src, flags=re.M)[1:]
    out = []
    for b in blocks:
        key = re.search(r'^\s*"([^"]+)"', b)
        desc = re.search(r'description="([^"]*)"', b)
        variants = re.findall(r'ToolVariant\(\s*key="([^"]+)"', b)
        default = re.search(r'default_variant="([^"]+)"', b)
        out.append({"key": key.group(1) if key else "?", "description": desc.group(1) if desc else "",
                    "variants": variants, "default_variant": default.group(1) if default else (variants[0] if variants else "")})
    return out


# ---------------------------------------------------------------- errors, environment, CLI, status, enums
def error_codes(codes_src: str, catalog_src: str) -> list[dict]:
    codes = {m.group(1): int(m.group(2)) for m in re.finditer(r"^\s+([A-Z][A-Z_]+) = (\d+)\s*$", codes_src, re.M)}
    for m in re.finditer(r"^\s+([A-Z][A-Z_]+) = _WALDOCTL_(\w+)", codes_src, re.M):
        codes[m.group(1)] = None          # waldoctl's shared number
    out = []
    for m in re.finditer(r"ErrorCode\.(\w+): _ErrorTemplate\((.*?)\n\s*\),", catalog_src, re.S):
        name, body = m.group(1), m.group(2)
        fields = {}
        for fm in re.finditer(r'(\w+)=((?:\s*"[^"]*")+)', body):
            fields[fm.group(1)] = "".join(re.findall(r'"([^"]*)"', fm.group(2)))
        out.append({"name": name, "code": codes.get(name), **{k: fields.get(k, "") for k in ("title", "cause", "effect", "remedy")}})
    known = {e["name"] for e in out}
    for name, code in codes.items():
        if name not in known:
            out.append({"name": name, "code": code, "title": "", "cause": "", "effect": "", "remedy": ""})
    return out


def env_vars(config_src: str) -> list[dict]:
    out = {}
    for m in re.finditer(r'os\.getenv\(\s*"(\w+)"\s*(?:,\s*("[^"]*"|[\w.()]+)\s*)?\)', config_src, re.S):
        default = m.group(2)
        if default is None:
            default = ""
        elif default.startswith('"'):
            default = default[1:-1]
        elif not re.fullmatch(r"[\d.]+", default):
            default = "computed"          # a path or an expression: see config.py
        out.setdefault(m.group(1), default)
    return [{"name": k, "default": v} for k, v in sorted(out.items())]


def cli_options(cli_src: str) -> list[dict]:
    out = []
    for m in re.finditer(r"add_argument\(\s*((?:\"[^\"]+\"\s*,?\s*)+)(.*?)\)\s*\n", cli_src, re.S):
        flags = re.findall(r'"([^"]+)"', m.group(1))
        rest = m.group(2)
        default = re.search(r"default=([^,\n)]+)", rest)
        help_ = re.search(r'help="([^"]*)"', rest)
        choices = re.search(r"choices=\[([^\]]*)\]", rest)
        action = re.search(r'action="([^"]*)"', rest)
        out.append({"flags": flags, "default": default.group(1).strip().strip('"') if default else "",
                    "help": help_.group(1) if help_ else "", "choices": re.findall(r'"([^"]+)"', choices.group(1)) if choices else [],
                    "action": action.group(1) if action else ""})
    return out


def status_fields(wire_src: str) -> list[dict]:
    tree = ast.parse(wire_src)
    cls = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "StatusBuffer")
    out = []
    for node in cls.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and not node.target.id.startswith("_"):
            default = ""
            if node.value is not None:
                v = ast.unparse(node.value)
                default = "" if v.startswith("field(") else v
            out.append({"name": node.target.id, "type": ast.unparse(node.annotation), "default": default})
    return out


def enum_names(wire_src: str, cls_name: str) -> list[str]:
    tree = ast.parse(wire_src)
    cls = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == cls_name)
    return [t.id for node in cls.body if isinstance(node, ast.Assign) for t in node.targets if isinstance(t, ast.Name)]


def profiles(methods: list[dict]) -> list[str]:
    for m in methods:
        if m["name"] == "select_profile":
            found = re.search(r"\(('[A-Z]+'(?:,\s*'[A-Z]+')*)\)", m["doc"])
            if found:
                return re.findall(r"'([A-Z]+)'", found.group(1))
    return []


# ---------------------------------------------------------------- the release notes
def release_notes(repository: str, out: Path) -> None:
    owner_repo = repository.rstrip("/").split("github.com/")[-1]
    req = urllib.request.Request(f"https://api.github.com/repos/{owner_repo}/releases?per_page=50",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "PAROL-docs sync_api"})
    with urllib.request.urlopen(req, timeout=30) as r:
        releases = json.load(r)
    lines = [f"<!-- Generated by tools/sync_api.py from the GitHub releases of {repository}. Do not edit. -->", ""]
    for rel in releases:
        if rel.get("draft"):
            continue
        body = (rel.get("body") or "").replace("\r\n", "\n").strip()
        body = re.sub(r"^(#{1,4}) ", lambda m: "#" * (len(m.group(1)) + 2) + " " if len(m.group(1)) < 4 else "##### ", body, flags=re.M)
        lines.append(f"### {rel['tag_name']} — {rel['published_at'][:10]}")
        lines.append("")
        lines.append(body or "*No release notes.*")
        lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- main
def build_facts(repo: Path, tag: str, repository: str) -> dict:
    sync_src, async_src = show(repo, tag, SYNC_CLIENT), show(repo, tag, ASYNC_CLIENT)
    methods = client_methods(sync_src, async_src)
    wire = show(repo, tag, WIRE)
    pyproject = show(repo, tag, PYPROJECT)
    proto = re.search(r"^PROTO_VERSION\s*=\s*(\d+)", wire, re.M)
    pyreq = re.search(r'requires-python\s*=\s*"([^"]+)"', pyproject)
    return {
        "generated_from": {"repository": repository, "tag": tag, "commit": git(repo, "rev-list", "-n", "1", tag).strip(),
                           "version": tag.lstrip("vV")},
        "python_requires": pyreq.group(1) if pyreq else "",
        "proto_version": int(proto.group(1)) if proto else None,
        "methods": methods,
        "tools": tool_methods(show(repo, tag, ROBOT)),
        "registered_tools": registered_tools(show(repo, tag, TOOLS)),
        "errors": error_codes(show(repo, tag, ERROR_CODES), show(repo, tag, ERROR_CATALOG)),
        "env": env_vars(show(repo, tag, CONFIG)),
        "cli": cli_options(show(repo, tag, CLI)),
        "status_fields": status_fields(wire),
        "cmd_types": enum_names(wire, "CmdType"),
        "query_types": enum_names(wire, "QueryType"),
        "profiles": profiles(methods),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--api", help=f"path to a clone of {REPO_NAME} (default: next to this repository, or API_DIR)")
    ap.add_argument("--check", action="store_true", help="exit 1 if api_facts.json is out of date; write nothing")
    ap.add_argument("--no-network", action="store_true", help="do not fetch the release notes")
    args = ap.parse_args()

    versions = yaml.safe_load((ROOT / "versions.yml").read_text(encoding="utf-8"))
    comp = versions["software"]["python_api"]
    tag, repository = str(comp["tag"]), str(comp["repository"])
    repo = find_api(args.api)
    git(repo, "rev-parse", "--verify", f"{tag}^{{commit}}")
    facts = build_facts(repo, tag, repository)
    text = json.dumps(facts, indent=2, ensure_ascii=False) + "\n"
    target = OUT / "api_facts.json"
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current.replace("\r\n", "\n") != text:
            print("api_facts.json is out of date: run python tools/sync_api.py")
            return 1
        print("api_facts.json is up to date")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {target.relative_to(ROOT)}: {len(facts['methods'])} methods, {len(facts['errors'])} error codes, "
          f"{len(facts['env'])} environment variables, {len(facts['registered_tools'])} tools (tag {tag})")
    if not args.no_network:
        try:
            release_notes(repository, OUT / "api_release_notes.md")
            print(f"wrote {(OUT / 'api_release_notes.md').relative_to(ROOT)}")
        except Exception as exc:  # noqa: BLE001
            print(f"release notes not fetched ({exc}); the file that is there is kept", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
