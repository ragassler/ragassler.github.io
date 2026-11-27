# Product

<!-- impeccable:product-schema 1 -->

Written without an interview (unattended run, 2026-11-27): facts come from
`site.toml`, `projects/*.md` and the README; lines marked *(inferred)* are
assumptions Ramura should confirm or correct.

## Platform

web

## Users

- Supervisors, research groups and hiring engineers in scientific computing / HPC
  who got Ramura's name from a CV, an application or a conversation and open the
  site to judge, in a few minutes, what she can actually do. *(inferred)*
- Mostly on a laptop at a desk; often a second look on a phone. *(inferred)*

## Product Purpose

Ramura Gassler's portfolio: one page that shows her theses, research work and
course projects in numerical PDE solvers and high-performance computing, with
the real simulations, plots, reports and code behind them. Success: a visitor
opens one or two projects, sees the results, and has a reason to contact her.

## Positioning

The work itself is the proof: simulations of a real Swiss dam break on
swisstopo terrain, multi-GPU scaling plots, roofline/flops numbers, theses as
PDFs. No neighbouring portfolio can show these exact results.

## Operating Context

Static site on GitHub Pages, built by `build.py` (Python standard library
only) from `site.toml` and `projects/*.md`. No JavaScript framework, no build
step besides `build.py`. Ramura edits the TOML/Markdown herself; Frederik
reviews through a feedback tool and opens issues.

## Capabilities and Constraints

- One page: intro + hero animation, highlight tiles, background timeline and
  tools, a filterable list of expandable projects.
- Media are MP4 loops (with JPEG posters), PNG plots and PDFs in `assets/`,
  copied in by `tools/sync_media.py`. Plots are matplotlib/COMSOL renders on
  white backgrounds.
- Content is Ramura's; facts only from the repo.

## Brand Commitments

None stated. The name, the ETH affiliation and the swisstopo credit must stay.

## Evidence on Hand

Project texts and media in `projects/*.md` and `assets/`; reports and slides in
`assets/pdf/`; public repos linked per project. No testimonials, no CV PDF yet
(`cv = ""`), no LinkedIn.

## Product Principles

1. Show the result, then the claim.
2. Every fact on the page traces to a file in the repo.
3. Easy for Ramura to edit without touching HTML or CSS.
4. Fast and readable on a phone.
