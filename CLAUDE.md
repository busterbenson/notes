# Claude Helper for busterbenson.com

## Build & Run Commands
- Build site: `bundle exec jekyll build`
- Run locally: `bundle exec jekyll serve --livereload`
- Watch for changes: `bundle exec jekyll serve --watch`
- Build production: `JEKYLL_ENV=production bundle exec jekyll build`
- Run specific tests: `bundle exec rspec spec/[specific_test_file].rb`

## Code Style Guidelines
- **Markdown:** Use YAML front matter for all content files
- **Front matter:** Required fields - layout, title, permalink
- **Images:** Store in /assets/images/ and use responsive_image tag
- **Collections:** Follow established collection structure (_pages, _posts, _mood, _tarot)
- **JavaScript:** Place in /assets/js/ directory
- **Naming:** Use kebab-case for filenames and slugs, always lower case as well
- **Layouts:** Reuse existing layouts in /_layouts/ directory
- **Links:** Use relative paths within the site
- **Images:** Use {% include img.html %} for responsive images

## Key Project Structure
Jekyll site with multiple collections (_posts, _mood, _tarot, etc.)

## Instructions for different directories
- When in the _tree directory, read _tree/instructions.md
- When in the _cosmology directory, read _cosmology/instructions.md
