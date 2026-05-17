# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project type

Personal academic website for Zihao Zhu, deployed straight from the repo root via GitHub Pages. **No build step, no npm, no Jekyll, no tests, no lint.** Plain HTML, CSS, vanilla JS, plus content in JS data files. `.nojekyll` disables Pages' Jekyll processing.

## Local preview

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`. Do not just open `blog.html`/`post.html` via `file://` — `post.html` `fetch()`s markdown at runtime and will fail on `file://` (the page detects this and prints a hint). The other pages render fine from the filesystem but use `http.server` to keep behavior consistent.

## Architecture

### One shared script, all pages

`script.js` runs unconditionally on every page and calls `renderHome()`, `renderPublicationsPage()`, `renderNewsPage()`, `renderTalksPage()`. Each function early-returns when its `[data-*]` target container is absent, so a single script handles every page. When adding a new section/page, follow the same pattern: add a `[data-something]` hook in HTML and a `render*` function that bails if the hook is missing.

`blog.js` is loaded only by `blog.html` and `post.html` and adds markdown rendering on top.

### Content lives in `data/*.js` as window globals

Each data file is a script tag, not a module — it just assigns to `window.SITE_*`:

- `data/publications.js` → `window.SITE_PUBLICATIONS` (array of papers)
- `data/news.js` → `window.SITE_NEWS`
- `data/talks.js` → `window.SITE_TALKS`
- `data/blog/index.js` → `window.SITE_BLOG_POSTS` (each entry's `file:` points to a markdown file under `data/blog/`)

`script.js` and `blog.js` read these globals via `window.SITE_* || []`. Adding content = editing the data file (and, for blog posts, dropping a markdown file alongside `data/blog/index.js`). Every HTML page that needs a given dataset must include its data script tag before `script.js` — see `index.html` for the full include list.

### Publication and news conventions

- **Selected publications** on the homepage are filtered by `selected: true` in `data/publications.js`. The full list page shows everything, with year tabs, topic chips, and a search box (`renderPublicationsPage`).
- **Sort orders**: publications sort year DESC, then title ASC. News, blog posts, and talks sort by date DESC.
- **Author highlighting**: `highlightAuthor()` automatically wraps the literal string `"Zihao Zhu"` in `<strong>`. Spell the name exactly that way in `authors:` arrays.
- **Topics** in `paper.topics` are free-form strings; the topic filter UI is generated from whatever appears across the dataset, so consistency matters (e.g. always `"Trustworthy AI"`, not `"trustworthy AI"`).
- **Link kinds** on a paper (`links: { paper, code, project, dataset, slides, press, ... }`) get icons via the `linkIcons`/`linkLabels` maps in `script.js`. Adding a new kind requires extending those maps (or it falls back to a generic external-link icon).

### Blog posts

`renderPostPage` (in `blog.js`) fetches `post.file` (a markdown path), strips YAML front matter, runs `marked` → `DOMPurify.sanitize` → injects into the page, then runs KaTeX auto-render and highlight.js. Relative image paths inside the markdown are rewritten relative to the markdown file's directory by `rewriteRelativeImages`. Headings get auto-generated IDs and a TOC.

When adding a post: add an entry to `data/blog/index.js` with a unique `slug`, and place the markdown file at the path given in `file:`.

### Theme toggle

`data-theme-toggle` button flips `document.documentElement.dataset.theme` between `""` and `"dark"`, persisted in `localStorage` under the key `theme`. All dark-mode styling hangs off the `[data-theme="dark"]` selector in `styles.css`.

### Vendor libs come from CDNs

lucide, iconify, marked, DOMPurify, KaTeX, and highlight.js are all loaded from `unpkg`/`jsdelivr` in the page `<script>`/`<link>` tags. There is no package.json. If you change versions, update every page that loads them.

### `brandfusion/` subdirectory

`brandfusion/` is a self-contained project landing page (its own `index.html` + assets, distinct from the main site's rendering pipeline). It's served at `/brandfusion/` on GitHub Pages and linked from publications via `links.project`. Treat it as an independent mini-site — don't try to integrate it with `script.js`.

## Editing checklist

- Adding a paper → edit `data/publications.js`. Set `selected: true` if it should appear on the homepage.
- Adding news → edit `data/news.js` (homepage shows the 5 most recent).
- Adding a talk → edit `data/talks.js`.
- Adding a blog post → add markdown under `data/blog/`, register it in `data/blog/index.js`.
- Changing layout/styles → `styles.css` is the single shared stylesheet; remember to check both light and dark themes.
- Adding a new page → copy an existing HTML file's `<head>` and `<header>` for consistent navigation, include the data scripts you need, and add a `render*` function in `script.js` (or a new dedicated script) keyed off a `[data-*]` hook.
