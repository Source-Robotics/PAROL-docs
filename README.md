# PAROL6 documentation

The documentation of the PAROL6 desktop robotic arm by [Source Robotics](https://source-robotics.com): the robot
manual (safety, technical data, installation, operation, tools, maintenance, the build guide), the control board
manual, the programming guide (concepts, the Python API, the commander software, ROS 2) and the API reference.

**Read it at [docs.source-robotics.com/PAROL-docs](https://docs.source-robotics.com/PAROL-docs/).**

The hardware files, the BOM and the control board firmware are in
[Source-Robotics/PAROL6-Desktop-robot-arm](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm); the
Python API in [PCrnjak/PAROL6-python-API](https://github.com/PCrnjak/PAROL6-python-API); the commander software in
[Source-Robotics/PAROL-commander-software](https://github.com/Source-Robotics/PAROL-commander-software).

## What is in this repository

| | |
|---|---|
| `docs/` | the pages: the robot manual at the top level (numbered chapters, `build/`, `appendix/`), `board/`, `end-effectors/`, `gui/`, `programming/` and `reference/` (one tab), `support/` |
| `docs/includes/` | text shared by pages (glossary, symbols, abbreviations) and the data the reference pages are built from |
| `docs/includes/generated/` | written by `tools/sync_api.py` from the Python API's release tag: `api_facts.json`, `api_release_notes.md`. Never edit |
| `docs/build/bill-of-materials.md`, `docs/assets/bom/` | written by `tools/sync_bom.py` from the robot repository's `BOM/BOM.md` and its reference images. Never edit |
| `versions.yml` | every version fact: the PAROL6 release the site describes, the software versions, the manuals' numbers and revisions |
| `compatibility.yml` | which control board, firmware, Python API, commander and gripper versions work together |
| `hooks/` | `versions.py` writes the version facts into the pages; `api_pages.py` builds the Python API reference |
| `tools/` | `sync_api.py`, `sync_bom.py`, `test_tools.py`, `root_404.html` |
| `overrides/` | the theme changes: the older-version banner, the edit/report line, the header's repository card |

The site is built with [MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme, in the same form as the
[PAR6](https://github.com/Source-Robotics/par6), [STEPFOC](https://github.com/Source-Robotics/STEPFOC-docs) and
gripper documentation; the hooks and tools follow the same pattern.

## Preview it locally

You need Python 3.11 or newer.

```bash
git clone https://github.com/Source-Robotics/PAROL-docs.git
cd PAROL-docs
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt      # Linux and macOS: .venv/bin/pip
mkdocs serve
```

Open `http://127.0.0.1:8000/PAROL-docs/`. The page reloads by itself when you save a file.

Every push and pull request runs `python tools/test_tools.py` and `mkdocs build --strict`, which fails on a broken
link or a missing page. Run both before you open a pull request.

## The API reference is generated from the Python API

The signatures and docstrings of every public method of the Python API's `RobotClient`, the tool methods, the
registered tools, the error codes, the environment variables and the controller's command line options are read
from the Python API's source **at its release tag** (`software.python_api.tag` in `versions.yml`) by
`tools/sync_api.py`. The reference pages under `docs/reference/python/` place each method with an
`<!-- api: name -->` marker and add the notes around it by hand; `hooks/api_pages.py` fills the markers in at
build time. The build fails on a marker naming a method the API does not have, and the tests fail when a public
method appears on no page.

```bash
python tools/sync_api.py            # write docs/includes/generated/ from software.python_api.tag in versions.yml
python tools/sync_api.py --check    # exit 1 if they are out of date
```

The tool needs a clone of the Python API repository with its tags, next to this repository or named by
`--api PATH` / `API_DIR`, and the network for the release notes (`--no-network` keeps the file that is there).
The CI build does not run it; the generated files are committed.

## The bill of materials is copied from the robot repository

`docs/build/bill-of-materials.md` is the robot repository's `BOM/BOM.md`, as it is, with its reference images
shown inline: `tools/sync_bom.py` reads a clone of `PAROL6-Desktop-robot-arm` (`--repo PATH`, `$PAROL6_DIR`, or a
sibling folder), converts the note blocks, copies and scales the images into `docs/assets/bom/`, and writes a
header naming the commit it copied. A wrong part or a broken link is fixed in the repository's file, then:

```bash
python tools/sync_bom.py            # rewrite the page and the images from the clone
python tools/sync_bom.py --check    # exit 1 if the page is out of date
```

## Versions and releases

Each PAROL6 release has its own version of this site, named after the release: `1`, ... The version selector in
the site's header switches between them, and a page of an older version says so in a bar at the top. The
versions are built with [mike](https://github.com/jimporter/mike) and kept in the `gh-pages` branch; `latest`
points at the newest.

**All version facts live in `versions.yml`, never in a page**: `docs_version` (the PAROL6 release these pages
describe, which is also the name the version is published under), `firmware.tag` (`V` + `docs_version`), the
software versions, and each manual's number, title, revision, status and publication date. `hooks/versions.py`
writes them into the version box on each document's landing page and into the list of documents on the About
page; a malformed or missing fact stops the build.

### When the Python API releases a new version

1. Set `software.python_api.tag` and `released` in `versions.yml`.
2. Run `python tools/sync_api.py`. If a method was added, the tests now fail until a reference page places it:
   add the marker and a note. If one was removed, the build fails on its marker: remove it.
3. Update the programming guide for what changed, using the release notes; give the Programming Guide a new
   revision letter in `versions.yml` and a line in its *Document history* on `docs/about.md`.
4. Commit and push to `main`.

### When PAROL6 releases a new version

1. Set `docs_version` and `firmware.tag` in `versions.yml`; add a row to `compatibility.yml`.
2. Update the pages for what changed; give the manuals new revision letters and document history lines.
3. Commit and push to `main`. The site publishes the new version, `latest` moves to it, and the previous version
   stays as it was.

### Publishing

`.github/workflows/publish.yml` publishes on every push to `main`: the tests, a strict build, then `mike deploy`
for `docs_version` with the alias `latest`. In the repository's Settings, under Pages, the source must be "Deploy
from a branch", branch `gh-pages`, folder `/ (root)`. Never run `mkdocs gh-deploy` on this repository: it would
overwrite every version mike keeps there.

The root of `gh-pages` also carries `404.html` (source: `tools/root_404.html`). It forwards addresses from before
the versioning, such as `/PAROL-docs/page4/`, to the same page under `latest/`, where the `redirects` plugin in
`mkdocs.yml` maps the old page names to the new pages. To preview the published versions locally, with the
version selector, run `mike serve`.

## The site's address

The site is served at `https://docs.source-robotics.com/PAROL-docs/`: the organisation's docs domain plus this
repository's name. Never rename this repository (its address would change and GitHub does not forward the old one),
and never add a `CNAME` file or a custom domain to it (that would take it out of the shared domain).

## License

- **Text and images:** [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/),
  see [LICENSE](LICENSE). You may copy, adapt and share them, also commercially, if you credit Source Robotics and
  share your changes under the same license.
- **Code:** the [MIT license](LICENSE-CODE). This covers the code examples in the pages and the site's own code
  (hooks, tools, overrides, scripts), so you can use an example in your own program without other conditions.
- **Names and logos:** the Source Robotics name, the product names and the logos are not covered by either license.
  The robot's hardware files, firmware and software are licensed separately, in their repositories (GPLv3).

By contributing you agree that your contribution is published under these licenses.

## Contributing

A small fix can be made from the browser: every page ends with a link to edit it on GitHub. For anything larger,
open an issue first, then a pull request. The *Contributing* page on the site has the house rules. Questions about
the robot itself go to the product repository's issue tracker.
