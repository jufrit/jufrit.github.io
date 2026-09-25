# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal site for Julian Fritsch, served by GitHub Pages at `jufrit.github.io` (repo pushed to `master` is deployed automatically). It is a minimal hand-rolled Jekyll site — no Gemfile, no theme, no plugins, no JS. Goal: a simple, clean public page for job hunting, with room to add personal projects later.

## Local preview

`sudo apt install jekyll` (Ubuntu), then `jekyll serve --livereload` → http://localhost:4000. Output goes to `_site/` (gitignored).

There are no tests or linters.

## Structure

- `_config.yml` — site name/description, kramdown, `exclude` list.
- `index.html` — the whole public site: a single page (hero, experience, education, toolkit) whose content mirrors `data/JulianFritsch_CV.pdf`. Keep the two in sync.
- `_layouts/default.html` — header nav (anchors into the home page + CV PDF), footer; loads Google Sans Flex / Google Sans Code from Google Fonts.
- `css/main.css` — single stylesheet; colors are CSS variables with a `prefers-color-scheme: dark` override. Visual direction is minimal, Google DeepMind-like (whitespace, light large headings, mono uppercase labels, pill links) — avoid generic template/AI-looking styles. Copy should be short and understated, not salesy; LinkedIn headline is "Machine Learning Engineer | PhD | Production AI & MLOps".
- `tools/make_images.py` — regenerates `data/social-card.png` (LinkedIn/link preview, referenced by the `og:image` tags in the layout) and `favicon.ico` / `apple-touch-icon.png`. Run `uv run --with pillow python tools/make_images.py`; its text constants must be updated when the headline changes.
- `data/` — CV PDF and portrait. Windows/Dropbox metadata files there are gitignored.

## Gotchas

- A file is only processed by Jekyll (layout + Liquid) if it starts with YAML front matter (`---`).
- GitHub Pages renders stray `.md` files even without front matter; anything not meant to be public (like this file) must be in `exclude` in `_config.yml`.
- Root-relative links (`/css/main.css`, `/data/...`) work because this is a user site (`<user>.github.io`) served at the domain root.
