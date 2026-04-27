source "https://rubygems.org"
# No `ruby` pin in the Gemfile — let .ruby-version drive (Netlify reads it).
# Local 4.0.2 builds use these stdlib pins; Netlify's 3.1.3 build doesn't
# need them but pulling the gems is harmless.

# Ruby 3.4+ moved a chunk of stdlib gems out of default load path; Ruby 4.0
# added ostruct to that list. Pinning here is harmless on Ruby 3.1/3.3
# (where they're still in stdlib) and required on Ruby 4.
gem 'bigdecimal'
gem 'observer'
gem 'csv'
gem 'base64'
gem 'mutex_m'
gem 'logger'
gem 'ostruct'
gem 'rmagick'
gem 'nokogiri', "~> 1.14.3"
gem 'jekyll'
gem 'jekyll-paginate'
gem 'jekyll-seo-tag'
gem 'jekyll-sitemap'
gem 'jekyll-target-blank'
gem 'jekyll-twitter-plugin'
gem 'jekyll-youtube'
gem 'jekyll-responsive-image'
gem 'jekyll-redirect-from'
gem 'jekyll-sass-converter', "~> 2.0"
gem 'jekyll-dotenv', '~> 0.1.0'
