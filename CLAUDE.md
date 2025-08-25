# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands
- Build site: `bundle exec jekyll build`
- Run locally: `bundle exec jekyll serve --livereload`
- Watch for changes: `bundle exec jekyll serve --watch`
- Build production: `JEKYLL_ENV=production bundle exec jekyll build`
- Debug config: `bundle exec jekyll doctor`
- Clear cache: `bundle exec jekyll clean`

## Architecture Overview

This is a Jekyll-powered personal website (busterbenson.com) with a complex collection-based architecture supporting multiple content systems:

### Core Collections
- `_posts/` - Blog posts organized by year (2003-2025), using layout: post
- `_pages/` - Static pages (about, links, etc.), using layout: page  
- `_mood/` - 64 binary mood states (nnnnnn.md to yyyyyy.md), using layout: mood
- `_tarot/` - Complete 78-card tarot deck with interpretations, using layout: tarot-card
- `_8bit/` - 8-bit oracle divination system with generated cards, using layout: 8bit-page
- `_trees/` - Tree identification system for California trees (see instructions.md)
- `_cosmology/` - Interview-based cosmology exploration system

### Jekyll Configuration Highlights
- Uses multiple specialized plugins: jekyll-responsive-image, jekyll-seo-tag, jekyll-target-blank
- Custom bidirectional linking system via `_plugins/bidirectional_links_generator.rb`
- Responsive image processing with multiple size outputs (480px, 800px, 1400px)
- Collections have custom permalinks (e.g., /mood/:name, /tarot/:name, /8bit/:name)

### Content Organization Patterns
- **Binary Systems**: Both `_mood/` and `_8bit/` use binary patterns for organization
- **Temporal Organization**: Posts organized chronologically with year-based directories
- **YAML Data**: Extensive use of `_data/` for structured content (navigation, symbols, etc.)
- **Generated Content**: `_8bit/` includes Python scripts for card generation and YAML-to-Markdown conversion

## Code Style Guidelines
- **Front Matter**: Required fields - layout, title, permalink
- **Naming**: Use kebab-case for filenames and slugs, always lowercase
- **Collections**: Follow established collection structure and layouts
- **Images**: Use `{% include img.html %}` for responsive images, store in /assets/images/
- **Links**: Use relative paths within the site
- **Layouts**: Reuse existing layouts in /_layouts/ directory (default, page, post, mood, tarot-card, etc.)

## Collection-Specific Instructions
- **_trees/**: Read _trees/instructions.md for comprehensive tree identification file generation guidelines
- **_cosmology/**: Read _cosmology/instructions.md for interview and decision tree workflows
- **_8bit/**: Card generation uses Python scripts in /cards/ directory with YAML templates
