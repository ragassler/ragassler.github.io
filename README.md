# Portfolio website

Source of <https://ragassler.github.io>. A small static site: one page with an
intro, highlight animations and an expandable list of projects.

## Layout

```
site.toml            name, intro, background, tools, hero + highlight media
projects/*.md        one file per project (TOML header between +++, then Markdown text)
assets/              css, js, and the media/PDFs shown on the site
tools/sync_media.py  copies media from the original project folders (run locally)
build.py             builds _site/ (standard-library Python only)
.github/workflows/   GitHub Actions: runs build.py and publishes on every push
```

## Everyday use

```sh
python3 build.py --serve      # preview at http://localhost:8000
python3 build.py --drafts     # include projects marked draft = true
git add -A && git commit -m "Update" && git push   # goes live in ~1 min
```

## Add a project

1. Copy one of `projects/*.md` and rename it. The number sets the file order; `order =` sets the page order.
2. Fill in the header (`title`, `summary`, `type`, `year`, `tags`, optional `[[media]]` and `[[links]]`).
3. Paste the abstract, README summary or intro as the text below the header.
4. For media, add a line to `MEDIA` in `tools/sync_media.py`, then run
   `python3 tools/sync_media.py`. Videos and GIFs become small MP4 files with a poster image.
5. `draft = true` keeps a project off the public page.
6. `featured = true` plus `thumb = "assets/…"` marks a project "Start here" and shows the
   thumbnail in the list (meant for two projects; give them the lowest `order`). In `site.toml`,
   `featured = true` on a highlight shows it large in the first row.

Topic filter buttons appear automatically for tags that occur in two or more projects.
