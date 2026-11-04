# The old manual, version 0 of the published site

The PAROL6 documentation as it was from 2023 to October 2026, before the site was rebuilt in the PAR6 form
(commit c24da4b1, 2026-10-29), stays readable in the version selector as "Old manual (2023 to October 2026)" at
https://docs.source-robotics.com/PAROL-docs/0/. It is not a release and is never updated.

It was built from commit 6d29879 (2026-10-22, the last commit of the old site) with `old-manual-v0.patch`, which
turns on the version selector, adds the bar "This is the old manual, kept for reference: the current manual is
here" and keeps search engines away (`noindex`). To build it again, in a worktree, never on main:

```
git worktree add ../old-manual 6d29879
cd ../old-manual
git apply <this repo>/tools/old-manual/old-manual-v0.patch
mike deploy 0 --title "Old manual (2023 to October 2026)"     # no alias, then push gh-pages
```

`mike delete 0` removes it. The publish workflow deploys only `docs_version` and `latest`, so it leaves 0 alone.
