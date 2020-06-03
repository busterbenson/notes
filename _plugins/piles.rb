module Jekyll
  class TagPageGenerator < Generator
    safe true

    def generate(site)
      piles = site.posts.docs.flat_map { |post| post.data['piles'] || [] }.to_set
      piles.each do |pile|
        site.pages << TagPage.new(site, site.source, pile)
      end
    end
  end

  class TagPage < Page
    def initialize(site, base, pile)
      @site = site
      @base = base
      @dir  = File.join('pile', pile)
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'pile.html')
      self.data['pile'] = pile
      self.data['title'] = "The #{pile} pile"
    end
  end
end