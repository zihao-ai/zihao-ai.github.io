# Zihao Zhu Personal Website

This repository contains the source for Zihao Zhu's personal academic website. It is a standalone static site for GitHub Pages and does not require Jekyll, npm, Ruby, or any build step.

## Preview Locally

Open `index.html` directly in a browser, or serve the repository root with any static file server:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Deploy

GitHub Pages can publish this repository directly from the root directory. The site is composed of plain HTML, CSS, JavaScript, and static assets.

## Files

- `index.html` - homepage with profile, selected publications, and recent news
- `publications.html` - full publication list with search, year filters, and topic filters
- `news.html` - full news timeline
- `cv.html` - academic CV page
- `styles.css` - shared visual system, layout, responsive styling, and dark mode
- `script.js` - shared rendering, publication filters, news rendering, theme toggle, and footer year
- `data/publications.js` - publication data source
- `data/news.js` - news data source
- `assets/` - local images and CV PDF

## Editing Content

Most content updates should be made in the data files:

- Add or edit papers in `data/publications.js`
- Add or edit news items in `data/news.js`

Homepage publications are controlled by the `selected` field in `data/publications.js`. Homepage news is rendered from the most recent items in `data/news.js`.
