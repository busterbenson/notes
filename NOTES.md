# Cool Tips

## Start the server
`bundle exec jekyll serve --incremental`

## Working with images (using webp)
- uses netlify's image_tag
- {% include img.html src=page.image alt=page.title %}

## Embedding tweets
- uses jekyll-twitter-plugin
- {% twitter https://twitter.com/buster/status/307895921197334528 data-conversation="none" %}