---
name: Ramura Gassler · Portfolio
description: One engineering drawing sheet that documents a body of numerical work.
colors:
  plotter-paper: "#f4f6f5"
  paper-tint: "#e8eceb"
  drawing-ink: "#121619"
  ink-secondary: "#3d454c"
  redline: "#c0161d"
  on-redline: "#ffffff"
  plot-white: "#ffffff"
  model-space: "#0d1317"
  model-space-tint: "#162027"
  model-ink: "#e4eae7"
  model-ink-secondary: "#a6b2ae"
  model-redline: "#ff5d52"
typography:
  name:
    fontFamily: "Barlow Semi Condensed, Barlow, Arial Narrow, sans-serif"
    fontSize: "clamp(2.5rem, 5.4vw, 4.4rem)"
    fontWeight: 600
    lineHeight: 0.95
    letterSpacing: "-0.01em"
  section-title:
    fontFamily: "Barlow Semi Condensed, Barlow, sans-serif"
    fontSize: "clamp(1.3rem, 2.2vw, 1.6rem)"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "0.04em"
  headline:
    fontFamily: "Barlow, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.35rem, 2.4vw, 1.85rem)"
    fontWeight: 500
    lineHeight: 1.2
  project-title:
    fontFamily: "Barlow, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.15rem, 1.9vw, 1.35rem)"
    fontWeight: 600
    lineHeight: 1.25
  body:
    fontFamily: "Barlow, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Barlow Semi Condensed, Barlow, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.08em"
rounded:
  none: "0px"
spacing:
  band: "26px"
  pad: "clamp(16px, 3.2vw, 44px)"
  cell: "8px 12px"
  section: "36px"
components:
  filter-cell:
    backgroundColor: "{colors.plotter-paper}"
    textColor: "{colors.drawing-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "10px 14px"
    height: "40px"
  filter-cell-active:
    backgroundColor: "{colors.redline}"
    textColor: "{colors.on-redline}"
  link-cell:
    backgroundColor: "{colors.plotter-paper}"
    textColor: "{colors.drawing-ink}"
    rounded: "{rounded.none}"
    padding: "12px 14px"
  link-cell-hover:
    backgroundColor: "{colors.drawing-ink}"
    textColor: "{colors.plotter-paper}"
  start-here:
    backgroundColor: "{colors.redline}"
    textColor: "{colors.on-redline}"
    typography: "{typography.label}"
---

# Design System: Ramura Gassler · Portfolio

## Overview

The page is one engineering drawing sheet. A thick frame and a hairline trim line
enclose everything; the band between them carries zone numbers (1–8) across the
top and a letter per section (A hero, B highlights, C background and tools,
D work) down the left. Identity lives in a title block, the simulations are placed
as labelled views, the timeline is a revision table and the tools are a parts
grid. The work's own images are colourful (jet, viridis, COMSOL); the sheet stays
ink-on-paper so they lead.

Light is plotter paper; dark is CAD model space (blue-black ground, pale ink).

## Colors

### Primary
- **Redline** `#c0161d` (dark: `#ff5d52`): state only. Active filter, open
  project (revision triangle and the filled toggle), "Start here", hover, focus.

### Neutral
- **Plotter paper** `#f4f6f5`, **paper tint** `#e8eceb` (featured rows, table
  heads), **drawing ink** `#121619` for every line and body text,
  **ink secondary** `#3d454c` for secondary text. Plots sit on **plot white**.

### Named Rules
- **The Redline Rule.** Red marks what is active or wanted now; it is never decoration.
- **The Ink Rule.** Lines are ink, never grey. Weight carries hierarchy: hairline
  1px (cells, rows), thin 1.5px (tables, section rules), thick 3px (frame, title block).

## Typography

Barlow (DIN-like technical grotesk) for everything; Barlow Semi Condensed in caps
for labels, section titles and metadata. Tabular numerals throughout. Code uses
the system monospace.

### Hierarchy
Name (h1, condensed, 2.5–4.4rem) › section titles (condensed caps with a thick
then thin underline, like a drawing view title) › headline › project titles ›
body 17px › labels 0.72rem caps.

## Layout

One sheet, max 1240px, padding `clamp(16px, 3.2vw, 44px)`. Sections run edge to
edge of the frame and are divided by thin rules that meet the zone ticks in the
band. Hero: title block, headline and intro on the left, the hero animation on the
right sized to its own aspect. Below 900px everything stacks and, on phones, the
hero animation moves up right after the headline. Below 640px the band narrows to 16px.

## Elevation & Depth

Flat. No shadows, no radii. Depth is line weight and the paper tint.

## Shapes

Rectangles only. The one non-rectangle is the red revision triangle on an open
project's title.

## Components

- **Title block**: grid of cells joined by hairlines inside a thick frame; name
  cell spans the top, labelled cells (Studies, Email, GitHub, …) below.
- **Filter cells / link cells**: square cells sharing borders, condensed caps.
  Active filter fills red; link cells fill ink on hover.
- **Project row**: title + summary, metadata column (type | year, tags as
  slash-separated condensed text), a square +/− toggle. Featured rows are tinted
  with a thumbnail carrying a red "Start here" band.
- **Revision table** (background) and **parts grid** (tools).
- **Note**: a bordered box with a "Note" label cell.

## Do's and Don'ts

### Do:
- Add content in `site.toml` / `projects/*.md`; the sheet adapts.
- Keep new elements as cells and rules in ink.

### Don't:
- Don't add pills, rounded cards, soft shadows or a mono "eyebrow" above headings.
- Don't use red for anything that isn't a state.
- Don't put a coloured bar down one side of a box; use a full border or a label cell.
