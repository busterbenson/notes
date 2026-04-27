# Internal Okayness — build-time score computation.
#
# Reads:  _data/okayness/tree.yml, _data/okayness/ratings.yml
# Writes: site.data.okayness.computed (a hash keyed by board id) for templates.
#
# Per board:
#   leaf_score / leaf_count — EWMA of own ratings, half-life = resilience_days
#   children_score          — weighted blend of child effective scores
#   effective_score         — final score shown on the dashboard
#   numb_streak_days        — consecutive days the most recent rating has been Numb
#   recent                  — last N ratings (for sparkline + notes)
#   trend                   — current EWMA minus EWMA-30-days-ago (signed delta)
#
# All scores are 0..7 floats. Boards with no ratings return nil for everything
# but children_score (still bubbles up children's scores).

require "date"

module OkaynessPlugin
  DEFAULT_RESILIENCE = 30
  DEFAULT_PARENT_WEIGHT = 0.0   # children fully dominate by default
  RECENT_LIMIT = 30

  class Generator < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      tree_data    = site.data.dig("okayness", "tree") || {}
      ratings_data = site.data.dig("okayness", "ratings") || {}
      blending     = tree_data["blending"] || {}

      themes = tree_data["themes"] || []
      ratings_by_id = (ratings_data["ratings"] || []).group_by { |r| r["id"] }

      now = Time.now
      computed = {}

      themes.each { |theme| compute_node(theme, now, ratings_by_id, blending, computed) }

      # Off-dashboard (GOD-residue) — projected GOD boards with no IOD presence
      # (or only fragmentary presence). Not rated, not scored — *named absences*.
      # Resolve `partial_into` board ids to their human names via `computed`
      # so the page template can render link text without re-walking the tree.
      off_dashboard = (tree_data["off_dashboard"] || []).map do |entry|
        resolved_partial = (entry["partial_into"] || []).map do |bid|
          { "id" => bid, "name" => (computed[bid] && computed[bid]["name"]) || bid }
        end
        entry.merge("partial_into_resolved" => resolved_partial)
      end

      # GOD coverage — count how many GOD nodes the IOD links to via god_anchor.
      # Walks every board + sub_dial in the live themes and collects unique
      # god_anchor ids; off_dashboard god_anchors count as "named absences"
      # that ARE in the GOD's universe (just not Tracked here).
      iod_anchors = collect_god_anchors(themes)
      off_anchors = (tree_data["off_dashboard"] || []).map { |e| e["god_anchor"] }.compact.uniq
      total_known_god_anchors = (iod_anchors + off_anchors).uniq

      site.data["okayness"] ||= {}
      site.data["okayness"]["computed"]      = computed
      site.data["okayness"]["themes_flat"]   = flatten(themes)
      site.data["okayness"]["off_dashboard"] = off_dashboard
      site.data["okayness"]["last_updated"]  = now.iso8601
      site.data["okayness"]["total_ratings"] = ratings_data["ratings"]&.length.to_i
      site.data["okayness"]["god_coverage"]  = {
        "linked"       => iod_anchors.size,
        "off_dashboard"=> off_anchors.size,
        "total_known"  => total_known_god_anchors.size,
      }
    end

    # Walk themes and pull every god_anchor — both on boards and on
    # nested sub_dials. Returns a unique list of GOD ids the IOD points at.
    def collect_god_anchors(nodes, out = [])
      nodes.each do |n|
        out << n["god_anchor"] if n["god_anchor"]
        collect_god_anchors(n["children"] || [], out) if n["children"]
        (n["sub_dials"] || []).each do |s|
          out << s["god_anchor"] if s["god_anchor"]
        end
      end
      out.compact.uniq
    end

    private

    def compute_node(node, now, ratings_by_id, blending, computed)
      id = node["id"]
      own_ratings = ratings_by_id[id] || []
      resilience = node["resilience_days"] || DEFAULT_RESILIENCE

      leaf_score, leaf_count = ewma(own_ratings, now, resilience)

      child_data = (node["children"] || []).map do |child|
        compute_node(child, now, ratings_by_id, blending, computed)
        computed[child["id"]]
      end

      child_blend = blend_children(child_data, blending[id])

      effective = combine_self_and_children(
        leaf_score, child_blend, blending[id]
      )

      now_score = leaf_score
      past_score, _ = ewma(own_ratings, now - 30 * 86400, resilience)
      trend = now_score && past_score ? (now_score - past_score).round(2) : nil

      computed[id] = {
        "id"               => id,
        "name"             => node["name"],
        "resilience_days"  => resilience,
        "leaf_score"       => leaf_score&.round(2),
        "leaf_count"       => leaf_count,
        "children_score"   => child_blend&.round(2),
        "effective_score"  => effective&.round(2),
        "effective_band"   => band_for(effective),
        "numb_streak_days" => numb_streak_days(own_ratings, now),
        "recent"           => own_ratings.sort_by { |r| r["at"].to_s }.last(RECENT_LIMIT),
        "trend"            => trend,
        # GOD-link surface — whether/how this IOD board points into the
        # canonical GOD tree. Personal-only boards have no god_anchor.
        "god_anchor"       => node["god_anchor"],
        "sub_dials"        => node["sub_dials"] || [],
      }
    end

    def ewma(ratings, ref_time, half_life_days)
      return [nil, 0] if ratings.empty?
      half_life_seconds = half_life_days * 86400.0
      total_w = 0.0
      total_ws = 0.0
      n = 0
      ratings.each do |r|
        rt = parse_time(r["at"])
        next if rt.nil? || rt > ref_time
        delta = (ref_time - rt).to_f
        w = 2 ** (-delta / half_life_seconds)
        total_w  += w
        total_ws += w * r["score"].to_f
        n += 1
      end
      return [nil, n] if total_w == 0.0
      [total_ws / total_w, n]
    end

    def blend_children(child_data, override)
      ranked = child_data.compact.select { |c| c["effective_score"] }
      return nil if ranked.empty?
      weights = (override && override["child_weights"]) || {}
      total_w = 0.0
      total_ws = 0.0
      ranked.each do |c|
        w = weights[c["id"]] || 1.0
        total_w  += w
        total_ws += w * c["effective_score"]
      end
      total_w == 0.0 ? nil : (total_ws / total_w)
    end

    def combine_self_and_children(leaf_score, child_blend, override)
      parent_weight = (override && override["parent_weight"]) || DEFAULT_PARENT_WEIGHT
      if child_blend && leaf_score
        parent_weight * leaf_score + (1 - parent_weight) * child_blend
      else
        child_blend || leaf_score
      end
    end

    def band_for(score)
      return "none" if score.nil?
      case score
      when 6.5..7.0 then "great"
      when 5.5..6.5 then "good"
      when 4.5..5.5 then "okay"
      when 3.5..4.5 then "neutral"
      when 2.5..3.5 then "not-okay"
      when 1.5..2.5 then "bad"
      when 0.5..1.5 then "terrible"
      else "numb"
      end
    end

    def numb_streak_days(ratings, now)
      sorted = ratings.sort_by { |r| r["at"].to_s }.reverse
      streak = 0
      sorted.each do |r|
        break unless r["score"].to_i == 0
        rt = parse_time(r["at"])
        next if rt.nil?
        days = ((now - rt) / 86400.0).floor
        streak = [streak, days + 1].max
      end
      streak
    end

    def parse_time(value)
      return value if value.is_a?(Time)
      Time.parse(value.to_s)
    rescue
      nil
    end

    def flatten(themes, depth = 0, out = [])
      themes.each do |node|
        out << { "id" => node["id"], "name" => node["name"], "depth" => depth }
        flatten(node["children"] || [], depth + 1, out) if node["children"]
      end
      out
    end
  end
end
