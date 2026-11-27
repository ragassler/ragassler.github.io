#!/usr/bin/env python3
"""Build the portfolio website into _site/.

    python3 build.py          # build
    python3 build.py --serve  # build and preview at http://localhost:8000

Content lives in:
    site.toml        name, intro, background, highlight animations
    projects/*.md    one file per project: TOML header between +++ lines,
                     then the text (Markdown) shown when the project is opened
    assets/          images, videos, PDFs (filled by tools/sync_media.py)

Only the Python standard library is used (Python >= 3.11 for tomllib).
"""
import html
import re
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"


# --------------------------------------------------------------------------
# Minimal Markdown: headings, paragraphs, lists, **bold**, *italic*, `code`,
# [links](url). Enough for project texts; raw HTML lines are passed through.
# --------------------------------------------------------------------------
def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{m.group(2)}"{ext_attr(m.group(2))}>{m.group(1)}</a>',
        text,
    )
    return text


def ext_attr(url):
    return ' target="_blank" rel="noopener"' if url.startswith("http") else ""


def markdown(src):
    out, para, items, list_tag = [], [], [], None

    def flush():
        nonlocal para, items, list_tag
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []
        if items:
            lis = "".join(f"<li>{inline(i)}</li>" for i in items)
            out.append(f"<{list_tag}>{lis}</{list_tag}>")
            items, list_tag = [], None

    for raw in src.strip().splitlines():
        line = raw.strip()
        if not line:
            flush()
        elif m := re.match(r"(#{2,4})\s+(.*)", line):
            flush()
            level = len(m.group(1)) + 1  # ## -> h3 (h2 is the section title)
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
        elif m := re.match(r"[-*]\s+(.*)", line):
            if para or list_tag == "ol":
                flush()
            list_tag = "ul"
            items.append(m.group(1))
        elif m := re.match(r"\d+\.\s+(.*)", line):
            if para or list_tag == "ul":
                flush()
            list_tag = "ol"
            items.append(m.group(1))
        elif line.startswith("<"):
            flush()
            out.append(line)
        elif items and raw.startswith((" ", "\t")):
            items[-1] += " " + line  # continuation of a list item
        else:
            if items:
                flush()
            para.append(line)
    flush()
    return "\n".join(out)


# --------------------------------------------------------------------------
# Content loading
# --------------------------------------------------------------------------
def load_projects(include_drafts=False):
    projects = []
    for path in sorted((ROOT / "projects").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"\+\+\+\n(.*?)\n\+\+\+\n(.*)", text, re.S)
        if not m:
            sys.exit(f"{path.name}: missing +++ TOML header +++")
        meta = tomllib.loads(m.group(1))
        meta["body"] = m.group(2)
        meta.setdefault("id", path.stem.split("-", 1)[-1])
        if meta.get("draft") and not include_drafts:
            print(f"  (draft, not published) {path.name}")
            continue
        projects.append(meta)
    return sorted(projects, key=lambda p: p.get("order", 100))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def media_html(m, cls=""):
    src = m["src"]
    cap = f"<figcaption>{inline(m['caption'])}</figcaption>" if m.get("caption") else ""
    alt = html.escape(m.get("alt", m.get("caption", "")), quote=True)
    if src.endswith(".mp4"):
        poster = m.get("poster", src[:-4] + ".jpg")
        el = (f'<video class="auto" src="{src}" poster="{poster}" muted loop playsinline '
              f'preload="none" aria-label="{alt}"></video>')
    else:
        el = f'<img src="{src}" alt="{alt}" loading="lazy">'
    return f'<figure class="{cls}"><div class="frame">{el}</div>{cap}</figure>'


def project_html(p):
    pid = p["id"]
    tags = "".join(f'<li data-tag="{slug(t)}">{html.escape(t)}</li>' for t in p.get("tags", []))
    tag_slugs = " ".join(slug(t) for t in p.get("tags", []))
    media = p.get("media", [])
    media_block = ""
    if media:
        cls = "media-grid one" if len(media) == 1 else "media-grid"
        media_block = f'<div class="{cls}">' + "".join(media_html(m) for m in media) + "</div>"
    links = "".join(
        f'<a class="btn" href="{l["url"]}"{ext_attr(l["url"])}>{html.escape(l["label"])}'
        f'<span aria-hidden="true">{" ↗" if l["url"].startswith("http") else " ↓"}</span></a>'
        for l in p.get("links", [])
    )
    note = f'<p class="note">{inline(p["note"])}</p>' if p.get("note") else ""
    featured = p.get("featured", False)
    thumb = ""
    if featured:
        img = f'<img src="{p["thumb"]}" alt="" loading="lazy">' if p.get("thumb") else ""
        thumb = f'<span class="p-thumb">{img}<span class="p-star">Start here</span></span>'
    return f"""
<details class="project{' featured' if featured else ''}" id="{pid}" data-tags="{tag_slugs}">
  <summary>
    {thumb}<span class="p-head">
      <span class="p-title">{inline(p['title'])}</span>
      <span class="p-sub">{inline(p.get('summary', ''))}</span>
    </span>
    <span class="p-meta">
      <span class="p-type">{html.escape(p.get('type', ''))}<span class="p-year">{html.escape(str(p.get('year', '')))}</span></span>
      <ul class="tags">{tags}</ul>
    </span>
    <span class="chev" aria-hidden="true"></span>
  </summary>
  <div class="p-body">
    {media_block}
    <div class="prose">{markdown(p['body'])}</div>
    {note}
    {f'<div class="links">{links}</div>' if links else ''}
  </div>
</details>"""


def page(site, projects):
    # filter chips: tags that occur in at least two projects
    counts = {}
    for p in projects:
        for t in p.get("tags", []):
            counts[t] = counts.get(t, 0) + 1
    chips = [t for t, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])) if c >= 2]
    chip_html = '<button class="chip on" data-filter="*">All</button>' + "".join(
        f'<button class="chip" data-filter="{slug(t)}">{html.escape(t)}</button>' for t in chips
    )

    bg = "".join(
        f'<li><span class="when">{html.escape(b["when"])}</span>'
        f'<span class="what">{inline(b["what"])}'
        + (f'<small>{inline(b["detail"])}</small>' if b.get("detail") else "")
        + "</span></li>"
        for b in site.get("background", [])
    )
    skills = "".join(f"<li>{html.escape(s)}</li>" for s in site.get("skills", []))

    contact = []
    if site.get("email"):
        contact.append(f'<a href="mailto:{site["email"]}">{html.escape(site["email"])}</a>')
    for key, label in (("github", "GitHub"), ("linkedin", "LinkedIn")):
        if site.get(key):
            contact.append(f'<a href="{site[key]}" target="_blank" rel="noopener">{label} ↗</a>')
    if site.get("cv"):
        contact.append(f'<a href="{site["cv"]}">CV (PDF) ↓</a>')

    hero = site["hero"]
    hero_html = media_html(hero, "hero-media")
    if hero.get("project"):
        hero_html = hero_html.replace(
            "<figcaption>",
            f'<figcaption><a class="jump" href="#{hero["project"]}">See project →</a> ', 1)

    tiles = "".join(
        f'<a class="tile{" featured" if h.get("featured") else ""}" href="#{h["project"]}">{media_html(h)}</a>'
        for h in site.get("highlights", [])
    )

    project_list = "\n".join(project_html(p) for p in projects)
    name = html.escape(site["name"])
    return TEMPLATE.format(
        name=name,
        description=html.escape(site.get("description", ""), quote=True),
        role=inline(site.get("role", "")),
        headline=inline(site.get("headline", "")),
        intro=markdown(site.get("intro", "")),
        background=bg,
        skills=skills,
        contact=" <span aria-hidden='true'>·</span> ".join(contact),
        hero=hero_html,
        tiles=tiles,
        chips=chip_html,
        projects=project_list,
        footer=inline(site.get("footer", "")),
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} · Portfolio</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{name} · Portfolio">
<meta property="og:description" content="{description}">
<meta property="og:image" content="assets/media/cleuson_2d_5m.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header class="hero wrap">
  <div class="intro">
    <p class="eyebrow">{role}</p>
    <h1>{name}</h1>
    <p class="headline">{headline}</p>
    <div class="prose">{intro}</div>
    <p class="contact">{contact}</p>
  </div>
  {hero}
</header>

<section class="wrap tiles" aria-label="Highlights">{tiles}</section>

<section class="wrap about" aria-label="Background">
  <div>
    <h2>Background</h2>
    <ol class="timeline">{background}</ol>
  </div>
  <div>
    <h2>Tools</h2>
    <ul class="skills">{skills}</ul>
  </div>
</section>

<main class="wrap" id="work">
  <div class="work-head">
    <h2>Selected work</h2>
    <p class="hint">Click a title to read the abstract or summary. Not sure where to begin? Try the two marked “Start here”.</p>
  </div>
  <div class="filters" role="group" aria-label="Filter by topic">{chips}</div>
  <div class="projects">
{projects}
  </div>
</main>

<footer class="wrap">{footer}</footer>
<script src="assets/js/site.js"></script>
</body>
</html>
"""


def build():
    site = tomllib.loads((ROOT / "site.toml").read_text(encoding="utf-8"))
    projects = load_projects(include_drafts="--drafts" in sys.argv)
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets",
                    ignore=shutil.ignore_patterns("_*"))
    (OUT / "index.html").write_text(page(site, projects), encoding="utf-8")
    (OUT / ".nojekyll").touch()
    # warn about media referenced but missing
    for ref in re.findall(r'(?:src|poster|href)="(assets/[^"]+)"', (OUT / "index.html").read_text()):
        if not (OUT / ref).exists():
            print(f"  WARNING: missing file {ref}")
    print(f"Built {len(projects)} projects -> {OUT / 'index.html'}")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Preview: http://localhost:8000  (Ctrl+C to stop)")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8000), handler).serve_forever()
