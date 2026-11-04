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
| `docs/assets/print_table.webp` | rendered by `tools/sync_print_table.py` from the robot repository's `Print table/Print_table.pdf`. Never edit |
| `versions.yml` | every version fact: the PAROL6 release the site describes, the software versions, the manuals' numbers and revisions |
| `compatibility.yml` | which control board, firmware, Python API, commander and gripper versions work together |
| `hooks/` | `versions.py` writes the version facts into the pages; `api_pages.py` builds the Python API reference; `llms.py` writes the Markdown twin of every page, `llms.txt` and `llms-full.txt` |
| `tools/` | `sync_api.py`, `sync_bom.py`, `sync_print_table.py`, `test_tools.py`, `root_404.html` |
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

## The bill of materials and the print table are copied from the robot repository

`docs/build/bill-of-materials.md` is the robot repository's `BOM/BOM.md`, as it is, with its reference images
shown inline: `tools/sync_bom.py` reads a clone of `PAROL6-Desktop-robot-arm` (`--repo PATH`, `$PAROL6_DIR`, or a
sibling folder), converts the note blocks, copies and scales the images into `docs/assets/bom/`, and writes a
header naming the commit it copied. A wrong part or a broken link is fixed in the repository's file, then:

```bash
python tools/sync_bom.py            # rewrite the page and the images from the clone
python tools/sync_bom.py --check    # exit 1 if the page is out of date
```

The print table on `docs/build/printing.md` is the owner's sheet as an image: `tools/sync_print_table.py` renders
`Print table/Print_table.pdf` of the same repository (exported from `PR_EXCEL.xlsx`) into `docs/assets/print_table.webp`,
cropped to the table (needs PyMuPDF and Pillow); the same `--repo` and `--check` options. Export the PDF again after
changing the spreadsheet.

## The 3D model, the Markdown twins and the "Last update" dates

`tools/build_model.py` builds `docs/assets/models/parol6/` from the PAROL6 URDFs in `urdf/parol6_description/` of a
clone of [robot_descriptions](https://github.com/Source-Robotics/robot_descriptions) (`--descriptions PATH`, else
`../../projects/robot_descriptions`; the system Python with `trimesh`, `fast-simplification` and `numpy`, and
`gltfpack` through `npx` to compress the files when Node.js is installed), the models the kinematics sheets come
from. The arm comes from `parol6_flange.urdf`, one GLB per moving link (the script first checks that all six variants
carry the same arm). Each variant gives one tool, `tool_<id>.glb`: everything `wrist_3_link` carries, in that
link's frame, with the fingers open. The tools are Flange only, Pneumatic gripper (the default), SSG-48, SSG-48
fin-ray, MSG and MSG soft jaws. In every file the meshes are merged per material and decimated for the web: the
printed parts (the URDF's structure colour) are the nodes named `<part>__body`, the only ones the reader recolours;
motors, jaws and the aluminium pneumatic gripper keep the model's colours. `viewer.json` holds the kinematic chain,
the tools and the defaults. The landing and kinematics pages show them in the arm viewer
`docs/javascripts/arm-viewer.js` (three.js from a CDN, through the import map in `overrides/main.html`, loaded
only on those pages): turn and zoom, a slider per joint within its limits, the gripper (each tool is fetched the
first time it is chosen) and the colour of the printed parts. Run the script again when the URDFs change.

`hooks/llms.py` writes, at every build, a Markdown twin of every page next to its HTML (`…/index.md`), `llms.txt`
(an index of the twins by tab) and `llms-full.txt` (every page in one file), with links pinned to the documented release (including when publishing with mike). The "Copy this page as Markdown" button in the page header reads the twin.

The "Last update" date under every page comes from the `git-revision-date-localized` plugin (the page's last
commit; the CI checks out the whole history for it). The calculator on Drives, ratios and resolution is
`docs/javascripts/joint-calculator.js`; the diagrams on the pages are Mermaid blocks in the Markdown.

## Analytics and comments

The "Was this page helpful?" widget at the end of every page is configured under `extra.analytics.feedback`.
With `provider: google` (the Google Analytics property all the docs sites share, loaded only after the reader
accepts the cookie banner of `extra.consent`), Material's own integration records the page views and sends each
vote as an event named `feedback`.

Comments under every page come from Giscus, wired in `overrides/partials/comments.html` and configured under
`extra.comments`: all the docs sites share one Discussions home, the hub repository
`Source-Robotics/source-robotics.github.io`, with one thread per site and page. A page opts out with
`comments: false` in its front matter (the landing page does).

## The PDF of the manual

The `print-site` plugin (the last plugin in `mkdocs.yml`) builds one page with every chapter in order, a cover and
a table of contents, at `print_page/`. `hooks/pdf.py` prints that page to `site/assets/PAROL6-manual.pdf` with headless
Chrome when the environment variable `DOCS_PDF` is set, which the publish workflow does; a local build sets it on
demand (`DOCS_PDF=1 mkdocs build`). While the hook is on, the page-help line of every page links the PDF.

## Versions and releases

Each PAROL6 release has its own version of this site, named after the release: `1`, ... The version selector in
the site's header switches between them, and a page of an older version says so in a bar at the top. The
versions are built with [mike](https://github.com/jimporter/mike) and kept in the `gh-pages` branch; `latest`
points at the newest. Version `0`, "Old manual (2023 to October 2026)", is the site from before the rebuild,
not a release: it is built from commit 6d29879 with a patch and must never be deployed from `main`
(`tools/old-manual/README.md`).

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

## Checking the page features

`python tools/test_site_features.py` checks release-pinned Markdown asset links, the prefilled issue body,
and the syntax of Python examples without running them or connecting to hardware. The CI build runs it.
