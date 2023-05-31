# https://bugfactory.io/blog/exposing-environment-variables-to-jekyll/
# Access env variables like site.env.VARIABLE
module Jekyll
  class EnvVariables < Generator
    def generate(site)
      site.config['env'] = {}
      ENV.each_pair { |k, v| site.config['env'][k] = v }
    end
  end
end