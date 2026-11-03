# Contributing

The documentation lives in [Source-Robotics/PAROL-docs](https://github.com/Source-Robotics/PAROL-docs). A small
fix, a typo, a wrong number, a missing link, can be made from the browser: every page ends with a link to edit it
on GitHub, which opens a pull request. For anything larger, open an issue first and say what you want to change.

## House rules

- Write for the reader who has the robot in front of them: what to do, in what order, and why when the why
  matters. Short sentences, one idea each.
- Facts come from the files: the firmware, the software's source, the BOM. When a page and the code disagree,
  the code is right and the page is fixed; a change to a command is made in the code first.
- Version facts live in `versions.yml`, never in a page. The API reference is generated from the Python API's
  source: edit the notes around the markers, not the markers' output.
- Link to a page of this site with its relative path, so that the build checks it; link to code on GitHub by
  its permanent URL.
- Images under 2400 px, with the exact file name (the live site is case-sensitive).
- Run `python tools/test_tools.py` and `mkdocs build --strict` before you open a pull request. Both run on every
  push.

The text and the images you contribute are published under CC BY-SA 4.0, the code examples under MIT.
