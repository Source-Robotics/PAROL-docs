#!/usr/bin/env python3
"""Tests for hooks/versions.py, hooks/api_pages.py and the shipped data files. No network, no API repository:
fixtures and the files in the repository. Run: python tools/test_tools.py (the build check runs it on every push)."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
fails = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"   [{detail}]" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hook = load_module("versions_hook", ROOT / "hooks" / "versions.py")
api = load_module("api_pages", ROOT / "hooks" / "api_pages.py")
from mkdocs.exceptions import PluginError  # noqa: E402

# ---------------------------------------------------------------- A. the version hook
GOOD = """docs_version: "1"
firmware: {name: PAROL6 release, repository: x, tag: V1}
software:
  python_api: {name: Python API (parol6), repository: y, tag: v0.9.1}
manuals:
  parol6: {number: SR-1002, title: PAROL6 Robot Manual, revision: 2026.A, status: draft, published: null, firmware: true,
           software: [python_api], applies_to: "PAROL6 V1", covers: the robot}
  guide: {number: SR-1101, title: Some Guide, revision: 2026.B, status: published, published: 2026-11-02,
          applies_to: "", covers: a guide}
"""


def load_text(text):
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
        f.write(text)
    try:
        return hook.load(f.name), None
    except PluginError as exc:
        return None, str(exc)
    finally:
        Path(f.name).unlink()


data, err = load_text(GOOD)
check("A1 a valid versions.yml loads", data is not None, err)
for label, bad, word in (
        ("docs_version not a release number", GOOD.replace('"1"', '"1.0"'), "docs_version"),
        ("a tag of another release", GOOD.replace("tag: V1}", "tag: V2}"), "does not belong"),
        ("a malformed tag", GOOD.replace("tag: V1}", "tag: 1}"), "firmware.tag"),
        ("a revision not YEAR.LETTER", GOOD.replace("2026.A", "A"), "YEAR.LETTER"),
        ("an unknown status", GOOD.replace("status: draft", "status: final"), "status"),
        ("published without a date", GOOD.replace("published: 2026-11-02", "published: null"), "publication date"),
        ("a missing field", GOOD.replace("covers: the robot", "covers: ''"), "lacks covers"),
        ("a software component without a tag", GOOD.replace("tag: v0.9.1", "tag: ''"), "lacks tag"),
        ("a manual listing unknown software", GOOD.replace("software: [python_api]", "software: [ros]"), "not under software")):
    d, e = load_text(bad)
    check(f"A2 refused: {label}", d is None and word in (e or ""), e)
meta = hook.meta_block("parol6", data)
check("A3 a release document's box: number, release, software version, revision (draft), applies to",
      "SR-1002" in meta and "**PAROL6 release:** 1" in meta and "**Python API (parol6):** v0.9.1" in meta
      and "2026.A (draft)" in meta and "**Applies to:** PAROL6 V1, PAROL6 release 1, Python API (parol6) v0.9.1" in meta, meta)
meta = hook.meta_block("guide", data)
check("A4 a published document's box: no release line, the date, no (draft)",
      "PAROL6 release" not in meta and "2026-11-02" in meta and "(draft)" not in meta, meta)
try:
    hook.meta_block("nope", data)
    check("A5 an unknown manual key stops the build", False)
except PluginError as exc:
    check("A5 an unknown manual key stops the build", "nope" in str(exc))
table = hook.documents_table(data)
check("A6 the documents table lists every manual", "SR-1002" in table and "SR-1101" in table and "PAROL6 release 1" in table)
vdata, err = load_text(GOOD + "models:\n  robot_descriptions: {name: robot_descriptions, repository: z, tag: v2.15.1}\n")
check("A8 a model version in running text: the tag without its v",
      vdata is not None and hook.version_text("models", "robot_descriptions", vdata) == "2.15.1", err)
try:
    hook.version_text("models", "nothing", vdata)
    check("A9 an unknown version placeholder stops the build", False, "no error")
except PluginError:
    check("A9 an unknown version placeholder stops the build", True)
_, err = load_text(GOOD + "models:\n  robot_descriptions: {name: robot_descriptions, repository: z}\n")
check("A10 a model without a tag stops the build", err is not None and "lacks tag" in err, err)
page = hook.URL_RE.sub(
    lambda m: hook.version_url(m.group(1), m.group(2), m.group(3), vdata),
    "[f](<!-- version-url: firmware -->/src) <!-- version-link: models.robot_descriptions -->")
check("A11 version-url is the files at the tag, version-link a link to them with the version as text",
      page == "[f](x/tree/V1/src) [2.15.1](z/tree/v2.15.1)", page)
sdata, _ = load_text(GOOD.replace("tag: v0.9.1}", "tag: v0.9.1, released: 2026-10-03}"))
check("A12 version-link adds the release date when there is one",
      sdata is not None and hook.version_url("link", "software", "python_api", sdata) == "[0.9.1](y/tree/v0.9.1) (2026-10-03)")
try:
    hook.version_url("url", "software", None, vdata)
    check("A13 a version-url without a component key stops the build", False, "no error")
except PluginError:
    check("A13 a version-url without a component key stops the build", True)
real, err = load_text((ROOT / "versions.yml").read_text(encoding="utf-8"))
check("A7 the repository's versions.yml loads", real is not None, err)

# ---------------------------------------------------------------- B. the API hook
FACTS = {
    "generated_from": {"repository": "r", "tag": "v0.9.1", "commit": "abc", "version": "0.9.1"},
    "methods": [
        {"name": "move_j", "category": "Motion", "property": False, "async_only": False, "returns": "int",
         "params": [{"name": "angles", "annotation": "list[float] | None", "default": "None", "kind": "positional"},
                    {"name": "*", "annotation": "", "default": None, "kind": "separator"},
                    {"name": "speed", "annotation": "float", "default": "0.5", "kind": "keyword-only"}],
         "doc": "Joint-space move.\n\nReturns the command index.\n\nCategory: Motion\n\nExample:\n    rbt.move_j([90, -90, 180, 0, 0, 180], speed=0.5)\n\nArgs:\n    angles: 6 joint angles in degrees\n        (ignored if pose= is set)\n    speed: Speed fraction in (0, 1]\n\nRaises:\n    MotionError: when refused\n"},
        {"name": "tool", "category": "Property", "property": True, "async_only": False, "returns": "SyncTool", "params": [],
         "doc": "Active bound tool."},
    ],
    "tools": {"electric": [{"name": "calibrate", "params": [{"name": "**kwargs", "annotation": "object", "default": None, "kind": "var-keyword"}],
                            "returns": "int", "doc": ""}], "pneumatic": []},
    "registered_tools": [{"key": "SSG-48", "description": "SSG-48 gripper", "variants": ["finger", "pinch"], "default_variant": "finger"}],
    "errors": [{"name": "MOTN_NOT_HOMED", "code": 35, "title": "Not homed", "cause": "c", "effect": "e", "remedy": "r"},
               {"name": "MOTN_CANCELLED", "code": None, "title": "Cancelled", "cause": "c", "effect": "e", "remedy": "r"}],
    "env": [{"name": "PAROL6_CONTROL_RATE_HZ", "default": "100"}],
    "cli": [{"flags": ["--port"], "default": "5001", "help": "UDP port", "choices": [], "action": ""}],
    "status_fields": [{"name": "angles", "type": "np.ndarray", "default": ""}],
    "profiles": ["TOPPRA", "RUCKIG"],
    "cmd_types": ["PING"], "query_types": ["PING"],
}
api._facts = FACTS
api._methods = {m["name"]: m for m in FACTS["methods"]}
api._pages = {"move_j": "reference/python/motion.md"}
api._compat = {"columns": [{"key": "release", "title": "Release"}], "rows": [{"release": "1"}]}
block = api.method_block("move_j")
check("B1 a method block: heading, signature with keyword-only star, defaults",
      "### `move_j`" in block and "rbt.move_j(angles: list[float] | None = None, *, speed: float = 0.5) -> int" in block, block)
check("B2 the docstring: paragraphs, an argument table with continuation lines, the example as code, raises as a list",
      "Joint-space move." in block and "| `angles` | 6 joint angles in degrees (ignored if pose= is set) |" in block
      and "```python\nrbt.move_j([90, -90, 180, 0, 0, 180], speed=0.5)\n```" in block and "- `MotionError`: when refused" in block
      and "Category" not in block, block)
check("B3 a property renders without a call", "```python\nrbt.tool\n```" in api.method_block("tool"))
try:
    api.method_block("fly")
    check("B4 an unknown method stops the build", False)
except PluginError as exc:
    check("B4 an unknown method stops the build", "fly" in str(exc))
tb = api.tool_block("electric", "calibrate")
check("B5 a tool method block", "### `tool.calibrate` (electric)" in tb and "rbt.tool.calibrate(**kwargs: object) -> int" in tb, tb)
try:
    api.tool_block("pneumatic", "calibrate")
    check("B6 an unknown tool method stops the build", False)
except PluginError as exc:
    check("B6 an unknown tool method stops the build", "calibrate" in str(exc))
idx = api.method_index()
check("B7 the method index links each method to its page", "| `move_j` | Motion | [motion](motion.md#move_j) |" in idx and "| `tool` | Property | — |" in idx, idx)
check("B8 the tools table puts the default variant first", "| `SSG-48` | SSG-48 gripper | `finger`, `pinch` |" in api.tools_table())
et = api.errors_table()
check("B9 the errors table: numbers, and 'shared' for waldoctl's code", "| `MOTN_NOT_HOMED` | 35 |" in et and "| `MOTN_CANCELLED` | shared |" in et, et)
check("B10 env, cli, status, profiles, version, compatibility tables render",
      "| `PAROL6_CONTROL_RATE_HZ` | `100` |" in api.env_table() and "| `--port` | `5001` | UDP port |" in api.cli_table()
      and "| `angles` | `np.ndarray` |" in api.status_fields() and api.profiles() == "`TOPPRA`, `RUCKIG`"
      and api.version() == "v0.9.1" and "| 1 |" in api.compat_table())
long_sig = api.signature("move_l", [{"name": n, "annotation": "float", "default": "0.0", "kind": "keyword-only"} for n in
                                    ("duration", "speed", "accel", "radius", "something", "another", "more")], "int")
check("B11 a long signature is wrapped one parameter per line", long_sig.startswith("rbt.move_l(\n    duration: float = 0.0,\n"), long_sig)

# ---------------------------------------------------------------- C. the shipped data files
facts_path = DOCS / "includes" / "generated" / "api_facts.json"
check("C1 api_facts.json is there", facts_path.exists())
if facts_path.exists():
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    tag = str(real["software"]["python_api"]["tag"]) if real else ""
    check("C2 the facts come from the tag versions.yml names", facts["generated_from"]["tag"] == tag,
          f"{facts['generated_from']['tag']} vs {tag}")
    markers: dict[str, list[str]] = {}
    for p in sorted((DOCS / "reference" / "python").glob("*.md")):
        for m in api.API_RE.finditer(p.read_text(encoding="utf-8")):
            markers.setdefault(m.group(1), []).append(p.name)
    public = {m["name"] for m in facts["methods"]}
    missing = sorted(public - set(markers))
    unknown = sorted(set(markers) - public)
    twice = sorted(n for n, ps in markers.items() if len(ps) > 1)
    check("C3 every public method of RobotClient is on a reference page", not missing, f"missing: {missing}")
    check("C4 every marker names a public method", not unknown, f"unknown: {unknown}")
    check("C5 no method is placed twice", not twice, f"twice: {twice}")
    tool_markers = {(m.group(1), m.group(2)) for p in (DOCS / "reference" / "python").glob("*.md")
                    for m in api.TOOL_RE.finditer(p.read_text(encoding="utf-8"))}
    tool_public = {(k, t["name"]) for k, ts in facts["tools"].items() for t in ts}
    check("C6 every tool method is on a reference page", tool_public <= tool_markers, f"missing: {sorted(tool_public - tool_markers)}")
    check("C7 the generated release notes are there", (DOCS / "includes" / "generated" / "api_release_notes.md").exists())
compat = yaml.safe_load((ROOT / "compatibility.yml").read_text(encoding="utf-8"))
check("C8 compatibility.yml has a row for docs_version",
      real is not None and any(str(r.get("release")) == real["docs_version"] for r in compat.get("rows", [])))
check("C9 compatibility.yml rows have every column", all(set(c["key"] for c in compat["columns"]) <= set(r) for r in compat["rows"]))

# ---------------------------------------------------------------- D. the pages
bad_links = []
for p in DOCS.rglob("*.md"):
    if "includes" in p.parts:
        continue
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r"\]\((https?://[^)\s]+)\)", t):
        if re.search(r"(source-robotics|pcrnjak)\.github\.io", m.group(1), re.I) or "github.com/PCrnjak/PAROL6-Desktop" in m.group(1) or "github.com/PCrnjak/PAROL-commander" in m.group(1):
            bad_links.append(f"{p.relative_to(DOCS)}: {m.group(1)}")
check("D1 no source-robotics.github.io addresses, no PCrnjak paths of repositories that moved to the organisation", not bad_links, "; ".join(bad_links[:5]))
odrive = [str(p.relative_to(DOCS)) for p in DOCS.rglob("*.md") if re.search(r"odrive|tinymovr", p.read_text(encoding="utf-8"), re.I)]
check("D2 no references to other vendors' documentation", not odrive, "; ".join(odrive))

# ---------------------------------------------------------------- E. the figures hook
fig = load_module("figures_hook", ROOT / "hooks" / "figures.py")
pair = "\n".join(["Text.", "", '![A robot](a.webp#only-light){ width="9" }',
                  '![A robot](a_dark.webp#only-dark){ width="9" }', "", "More."])
out, n = fig.transform(pair, 1, "3.")
check("E1 a light and a dark picture are one figure, numbered on from the chapter's count, alt text as caption",
      n == 1 and out.count("<figure") == 1 and "<figcaption>Figure 3.2: A robot.</figcaption>" in out, out)
inline = "\n".join(["A line of text", "![A robot](a.webp)", "", "![Hero](h.webp){ .hero }", ""])
out, n = fig.transform(inline, 0, "")
check("E2 a picture inside a paragraph and a hero picture are left alone", n == 0 and "<figure" not in out, out)
check("E3 numbered chapters count across pages, other pages on their own",
      fig.chapter("03-technical-data/joint-limits.md") == ("03-technical-data", "3.")
      and fig.chapter("board/05-stepper-drivers.md") == ("board/05-stepper-drivers.md", "5.")
      and fig.chapter("theory/kinematics.md") == ("theory/kinematics.md", ""))

# ---------------------------------------------------------------- F. the known issues hook
ki = load_module("known_issues_hook", ROOT / "hooks" / "known_issues.py")
try:
    shipped, err = ki.load(ROOT / "known_issues.yml", DOCS), None
except PluginError as exc:
    shipped, err = None, str(exc)
check("F1 known_issues.yml loads, and every issue's page exists", shipped is not None, err)
check("F2 an issue's link is relative to the page it lands on",
      ki.link({"page": "board/09-test-firmware.md#commands", "title": "T"}, "08-troubleshooting/known-issues.md")
      == "[T](../board/09-test-firmware.md#commands)")
ISSUE = {"id": "KI-1", "component": "c", "summary": "s", "workaround": "w", "page": "index.md", "title": "t",
         "status": "open", "since": "2026-11-02"}


def load_issues(issues):
    text = yaml.safe_dump({"components": {"c": {"name": "C", "version": "1"}}, "issues": issues})
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
        f.write(text.replace("'2026-11-02'", "2026-11-02"))
    try:
        return ki.load(f.name, DOCS), None
    except PluginError as exc:
        return None, str(exc)
    finally:
        Path(f.name).unlink()


_, err = load_issues([dict(ISSUE, component="x")])
check("F3 an unknown component stops the build", err is not None and "not under components" in err, err)
_, err = load_issues([ISSUE, dict(ISSUE)])
check("F4 a repeated id stops the build", err is not None and "twice" in err, err)
data, err = load_issues([ISSUE, dict(ISSUE, id="KI-2", status="fixed", fixed_in="1.1")])
out = ki.all_issues(data, "08-troubleshooting/known-issues.md") if data else ""
check("F5 open issues are listed by component, fixed ones under Fixed with their version",
      "### C" in out and "### Fixed" in out and "| KI-2 | s | 1.1 |" in out and "| KI-1 | s | w |" in out, err or out)

print()
if fails:
    print(f"{len(fails)} failed: " + ", ".join(fails))
    sys.exit(1)
print("all passed")
