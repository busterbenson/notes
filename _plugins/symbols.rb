module Jekyll
  class SymbolPageGenerator < Generator
    safe true

    def generate(site)
      symbols = site.data['symbols']
      tarot_cards = site.collections['tarot'].docs
      symbols.each do |symbol|
        docs = tarot_cards.filter{|c|c.data['symbols'] and c.data['symbols'].include?(symbol[0])}
        site.pages << SymbolPage.new(site, site.source, symbol[0], symbol[1], docs)
      end
    end
  end

  class SymbolPage < Page
    def initialize(site, base, symbol, symbol_data, docs)
      # Jekyll.logger.warn symbol.inspect
      @site = site
      @base = base
      @dir  = File.join('symbol', symbol)
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'symbol.html')
      self.data['symbol'] = symbol
      self.data['symbol_data'] = symbol_data
      self.data['title'] = "Symbol: #{symbol_data['name']}"
      self.data['cards'] = docs
    end
  end
end