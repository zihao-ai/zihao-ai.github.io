# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **al-folio** Jekyll-based academic portfolio website for Zihao Zhu, deployed at https://zihao-ai.github.io. It showcases research, publications, projects, and blog posts.

## Development Commands

```bash
# Local development with Docker (RECOMMENDED)
docker compose pull
docker compose up
# Site available at http://localhost:8080 with live reload on port 35729

# Alternative: slim Docker image
docker compose -f docker-compose-slim.yml up

# Manual Jekyll commands (requires Ruby environment)
bundle exec jekyll build                    # Build site to _site/
bundle exec jekyll serve --port=8080        # Serve with live reload
JEKYLL_ENV=production bundle exec jekyll build  # Production build
```

## Architecture

**Framework:** Jekyll static site generator with Liquid templates

**Key Directories:**
- `_pages/` - Main site pages (about.md, cv.md, publications.md, projects.md)
- `_bibliography/papers.bib` - BibTeX publications (processed by jekyll-scholar)
- `_data/` - YAML data files (cv.yml, socials.yml, repositories.yml, coauthors.yml)
- `_layouts/` - Liquid template layouts
- `_includes/` - Reusable template components
- `_projects/` - Research project markdown files
- `_posts/` - Blog posts (excluded from build by default in _config.yml)
- `_sass/` - SCSS stylesheets
- `_plugins/` - Custom Ruby plugins (Google Scholar citations, etc.)
- `assets/` - Static assets (images, PDFs, CSS, JS)

**Configuration:**
- `_config.yml` - Main Jekyll config, theme settings, plugin config, scholar settings
- `Gemfile` - Ruby gem dependencies

## Jekyll Scholar

Publications are managed via BibTeX in `_bibliography/papers.bib`. The `scholar` section in `_config.yml` controls:
- Author highlighting: `last_name: [Zhu]`, `first_name: [Zihao]`
- Bibliography style: APA
- Grouping: by year, descending

Special BibTeX fields for al-folio: `abbr`, `abstract`, `arxiv`, `code`, `pdf`, `poster`, `slides`, `video`, `website`, `preview`, `selected`, `award`, `award_name`

## Build Pipeline

GitHub Actions (`.github/workflows/deploy.yml`) handles deployment:
1. Ruby 3.3.5 + Python 3.13 setup
2. ImageMagick for responsive image generation
3. Jekyll build with production environment
4. CSS purging via purgecss
5. Deploy to GitHub Pages

## Code Style

Prettier is used for code formatting (checked in CI via `.github/workflows/prettier.yml`). Configuration in `.prettierrc`.
