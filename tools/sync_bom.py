#!/usr/bin/env python3
"""Copy the robot repository's bill of materials into the docs, as it is.

    python tools/sync_bom.py [--repo PATH] [--check]

Reads BOM/BOM.md and BOM/BOM reference images/ from a clone of PAROL6-Desktop-robot-arm (--repo, else $PAROL6_DIR,
else a sibling folder of this repository or ../../projects), and writes docs/build/bill-of-materials.md and
docs/assets/bom/. The page is the repository's file with these changes only:

  - a header that names the original and the commit it was copied from
  - GitHub's `> [!NOTE]` blocks become admonitions
  - the "Reference Image" links become small inline pictures (click to enlarge), the images scaled to 400 px
  - links into the repository (../STL/...) become absolute, and PCrnjak/ paths become Source-Robotics/

Everything else, the parts, the quantities, the purchase links, is left untouched: a wrong part is fixed in the
repository's BOM.md, then this tool is run again. --check exits 1 when the page is out of date.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "build" / "bill-of-materials.md"
IMG_DIR = ROOT / "docs" / "assets" / "bom"
REPO_URL = "https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm"
THUMB = 120      # px shown in the table
STORED = 400     # px long side of the stored copy

HEADER = """# Bill of materials

!!! note "This is a copy"
    The original is [BOM/BOM.md]({url}/blob/main/BOM/BOM.md) in the robot's repository; this page is that
    file as of {when} (commit `{commit}`), with the reference images shown inline. If a link is broken or a part
    is wrong, [open an issue]({url}/issues/new) there, and the fix lands here with the next sync.

"""


def find_repo(arg: str | None) -> Path:
    candidates = [arg, os.environ.get("PAROL6_DIR"), ROOT.parent / "PAROL6-Desktop-robot-arm",
                  ROOT.parent.parent / "projects" / "PAROL6-Desktop-robot-arm"]
    for c in candidates:
        if c and (Path(c) / "BOM" / "BOM.md").exists():
            return Path(c)
    sys.exit("sync_bom: no clone of PAROL6-Desktop-robot-arm found; pass --repo PATH")


def safe_name(name: str) -> str:
    stem, ext = os.path.splitext(name)
    return re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_") + ext.lower()


def convert(text: str, repo: Path, write_images: bool) -> str:
    text = text.replace("\r\n", "\n")
    # the title: ours
    text = re.sub(r"\A# .*?\n+This file contains all the parts you need to build the PAROL6 robot!\n+", "", text)
    # GitHub note blocks -> admonitions
    def note(m):
        body = " ".join(line.lstrip("> ").strip() for line in m.group(1).split("\n") if line.strip())
        return f"!!! note\n    {body}\n"
    text = re.sub(r"> \[!NOTE\]\n((?:>.*\n?)+)", note, text)
    # horizontal rules: the headings separate the sections
    text = re.sub(r"\n---\n", "\n", text)
    # repository-relative links
    text = text.replace("](../STL/", f"]({REPO_URL}/tree/main/STL/")
    text = text.replace("github.com/PCrnjak/PAROL6-Desktop-robot-arm", "github.com/Source-Robotics/PAROL6-Desktop-robot-arm")
    # reference images -> thumbnails
    img_src = repo / "BOM" / "BOM reference images"
    used: dict[str, str] = {}

    def image(m):
        rel = m.group(1).replace("%20", " ")
        name = Path(rel).name
        safe = safe_name(name)
        src = img_src / name
        if not src.exists():
            sys.exit(f"sync_bom: BOM.md refers to a missing image: {name}")
        used[name] = safe
        return f'![{Path(name).stem}](../assets/bom/{safe}){{ width="{THUMB}" }}'
    text = re.sub(r"\[Link\]\(BOM%20reference%20images/([^)]+)\)", image, text)
    if write_images:
        from PIL import Image
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        for old in IMG_DIR.iterdir():
            if old.name not in used.values():
                old.unlink()
        for name, safe in used.items():
            im = Image.open(img_src / name)
            im = im.convert("RGB") if safe.endswith(".jpg") else im.convert("RGBA")
            im.thumbnail((STORED, STORED))
            im.save(IMG_DIR / safe, optimize=True)
    return text.strip() + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="the clone of PAROL6-Desktop-robot-arm")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 when the page is out of date")
    args = ap.parse_args(argv)
    repo = find_repo(args.repo)
    try:
        commit, when = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%h %cs", "--", "BOM/BOM.md"],
                                      capture_output=True, text=True, check=True).stdout.split()
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        commit, when = "unknown", "today"
    body = convert((repo / "BOM" / "BOM.md").read_text(encoding="utf-8"), repo, write_images=not args.check)
    page = (HEADER.format(url=REPO_URL, when=when, commit=commit) + body).replace("\n", "\r\n")
    if args.check:
        current = PAGE.read_bytes().decode("utf-8") if PAGE.exists() else ""
        # the commit line changes with every repository commit that touches the file; compare the body only
        same = current.split("\r\n\r\n", 2)[-1:] == page.split("\r\n\r\n", 2)[-1:]
        print("bill-of-materials.md is " + ("up to date" if same else "OUT OF DATE: run tools/sync_bom.py"))
        return 0 if same else 1
    PAGE.write_bytes(page.encode("utf-8"))
    print(f"wrote {PAGE.relative_to(ROOT)} from {repo} ({commit}, {when}); {len(list(IMG_DIR.iterdir()))} reference images")
    return 0


if __name__ == "__main__":
    sys.exit(main())
