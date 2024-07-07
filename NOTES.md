# Cool Tips

## Build the site
`bundle exec jekyll build`

## Start the server 
`ruby -v`
`rvm use 2.7.7` (if `rvm list` shows 2.3.4 or 2.6.3 is being used)
`bundle exec jekyll serve --incremental`
http://localhost:4000

## Working with images (using webp)
- uses netlify's image_tag
- {% include img.html src=page.image alt=page.title %}

## Embedding tweets
- uses jekyll-twitter-plugin
- {% twitter https://twitter.com/buster/status/307895921197334528 data-conversation="none" %}