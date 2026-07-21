# Syncs _data/questions.json from the "Question Game" Google Sheet at build
# time, so every deploy ships the current spreadsheet contents. The checked-in
# snapshot is the fallback: if the fetch fails or the result looks wrong
# (sheet made private, columns renamed, suspicious shrinkage), the build keeps
# the snapshot and logs a warning instead of shipping a broken page.
#
# The sheet must remain link-accessible (Share -> anyone with the link) for
# the unauthenticated CSV export to work. Set QUESTIONS_SKIP_FETCH=1 to skip
# the network entirely (e.g. offline local builds).
#
# Sync rules (mirroring how the page was originally built):
#   - a row is included when its "Include?" cell starts with Y (Y/YY/YYY)
#   - category is "New Category", falling back to "Category", with trailing
#     "(1)"-style suffixes stripped (e.g. "Perception (1)" -> "Perception")
#   - sheets/tabs are discovered automatically; any tab with "Question" and
#     "Include?" columns participates, so new tabs of questions just work

require 'net/http'
require 'uri'
require 'csv'
require 'json'

module QuestionsFetcher
  SHEET_ID = '15LvRy4jxRn7S6uMWl4u2vZNKkppAeI-tHCtCnQWzqkI'
  DATA_PATH = File.expand_path('../_data/questions.json', __dir__)
  TIMEOUT_SECONDS = 15
  MIN_QUESTIONS = 100

  def self.http_get(url, redirects_left = 5)
    raise 'too many redirects' if redirects_left.zero?
    uri = URI(url)
    response = Net::HTTP.start(uri.host, uri.port, use_ssl: true,
                               open_timeout: TIMEOUT_SECONDS, read_timeout: TIMEOUT_SECONDS) do |http|
      http.get(uri.request_uri)
    end
    case response
    when Net::HTTPRedirection
      http_get(URI.join(url, response['location']).to_s, redirects_left - 1)
    when Net::HTTPSuccess
      response.body
    else
      raise "HTTP #{response.code} for #{uri.host}"
    end
  end

  # The htmlview page lists every tab's gid; candidate gids that aren't real
  # question tabs are filtered out by the header check in parse_sheet.
  def self.candidate_gids
    html = http_get("https://docs.google.com/spreadsheets/d/#{SHEET_ID}/htmlview")
    gids = html.scan(/gid[=:]\s*"?(\d+)/).flatten.uniq
    gids.empty? ? ['0'] : gids
  end

  def self.parse_sheet(csv_text)
    rows = CSV.parse(csv_text)
    header_index = rows.index { |r| r&.map(&:to_s)&.include?('Question') }
    return [] unless header_index
    headers = rows[header_index].map(&:to_s)
    q_col   = headers.index('Question')
    inc_col = headers.index('Include?')
    cat_col = headers.index('Category')
    new_col = headers.index('New Category')
    return [] unless q_col && inc_col

    rows.drop(header_index + 1).filter_map do |row|
      next unless row
      question = row[q_col].to_s.strip
      next if question.empty?
      next unless row[inc_col].to_s.strip.upcase.start_with?('Y')
      category = new_col ? row[new_col].to_s.strip : ''
      category = row[cat_col].to_s.strip if category.empty? && cat_col
      category = category.sub(/\s*\(\d+\)\s*\z/, '')
      { 'q' => question, 'c' => category }
    end
  end

  def self.fetch_questions
    candidate_gids.flat_map do |gid|
      parse_sheet(http_get("https://docs.google.com/spreadsheets/d/#{SHEET_ID}/export?format=csv&gid=#{gid}"))
    end.uniq { |item| item['q'] }
  end

  def self.run
    if ENV['QUESTIONS_SKIP_FETCH'] == '1'
      Jekyll.logger.info 'Questions:', 'QUESTIONS_SKIP_FETCH=1, using checked-in snapshot'
      return
    end
    items = fetch_questions
    raise "only #{items.size} questions found (need >= #{MIN_QUESTIONS})" if items.size < MIN_QUESTIONS
    previous = begin
      JSON.parse(File.read(DATA_PATH))
    rescue StandardError
      []
    end
    raise "count dropped #{previous.size} -> #{items.size}" if items.size < previous.size / 2

    if items == previous
      Jekyll.logger.info 'Questions:', "spreadsheet unchanged (#{items.size} questions)"
    else
      File.write(DATA_PATH, JSON.pretty_generate(items) + "\n")
      Jekyll.logger.info 'Questions:', "synced #{items.size} questions from spreadsheet (was #{previous.size})"
    end
  rescue StandardError => e
    Jekyll.logger.warn 'Questions:', "fetch failed, using checked-in snapshot (#{e.message})"
  end
end

# after_init runs before Jekyll reads _data, so the freshly-synced file is
# what site.data.questions picks up.
Jekyll::Hooks.register :site, :after_init do |_site|
  QuestionsFetcher.run
end
