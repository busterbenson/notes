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
      god_data     = site.data.dig("okayness", "god_tree") || {}
      blending     = tree_data["blending"] || {}

      themes = tree_data["themes"] || []
      ratings_by_id = (ratings_data["ratings"] || []).group_by { |r| r["id"] }

      now = Time.now
      computed = {}

      themes.each { |theme| compute_node(theme, now, ratings_by_id, blending, computed) }

      # Off-dashboard (GOD-residue) — IOD-side metadata about *why* certain
      # GOD nodes aren't tracked. Not rated, not scored — *named absences*.
      # Lives here (option a from the design doc): GOD structure stays clean
      # in god_tree.yml; IOD-specific status / partial_into / note fields stay
      # in tree.yml under off_dashboard. The Full-GOD tree section below reads
      # from BOTH plus tree.yml's god_anchor fields to render linkage state.
      # Resolve `partial_into` board ids to their human names via `computed`
      # so the template can render link text without re-walking the tree.
      off_dashboard = (tree_data["off_dashboard"] || []).map do |entry|
        resolved_partial = (entry["partial_into"] || []).map do |bid|
          { "id" => bid, "name" => (computed[bid] && computed[bid]["name"]) || bid }
        end
        entry.merge("partial_into_resolved" => resolved_partial)
      end
      off_dashboard_by_anchor = off_dashboard
        .each_with_object({}) { |e, h| h[e["god_anchor"]] = e if e["god_anchor"] }

      # GOD coverage — collect every god_anchor referenced from the live IOD,
      # then walk the canonical god_tree.yml so we know the full universe of
      # GOD nodes (board + dial). For each GOD node we compute a linkage
      # state: linked / partial / not-linked / numb. The Full-GOD section in
      # the page template renders this tree.
      iod_anchors_with_owners = collect_iod_anchor_owners(themes, computed)
      iod_anchor_ids = iod_anchors_with_owners.keys

      god_render = build_god_tree_render(
        god_data,
        iod_anchors_with_owners,
        off_dashboard_by_anchor,
      )

      total_known_god_anchors = (iod_anchor_ids + off_dashboard.map { |e| e["god_anchor"] }.compact).uniq

      site.data["okayness"] ||= {}
      site.data["okayness"]["computed"]      = computed
      site.data["okayness"]["themes_flat"]   = flatten(themes)
      site.data["okayness"]["off_dashboard"] = off_dashboard
      site.data["okayness"]["god_render"]    = god_render
      site.data["okayness"]["last_updated"]  = now.iso8601
      site.data["okayness"]["total_ratings"] = ratings_data["ratings"]&.length.to_i
      site.data["okayness"]["god_coverage"]  = {
        "linked"       => iod_anchor_ids.size,
        "off_dashboard"=> off_dashboard.size,
        "total_known"  => total_known_god_anchors.size,
        "totals"       => god_render["totals"],
      }
    end

    # Walk themes and collect every god_anchor mapping. Returns a hash:
    #   { "<god-anchor-id>" => [ { "id" => iod_id, "name" => iod_name }, ... ] }
    # so the GOD render can show *which* IOD board(s) link to a given GOD
    # node. A GOD anchor can be linked from more than one IOD board (the
    # canonical example: markets/macro is linked from both Budget and
    # Investments).
    def collect_iod_anchor_owners(nodes, computed, owners = {}, parent_owner = nil)
      nodes.each do |n|
        node_owner = if computed[n["id"]]
                       { "id" => n["id"], "name" => computed[n["id"]]["name"] || n["name"] }
                     else
                       { "id" => n["id"], "name" => n["name"] }
                     end
        if n["god_anchor"]
          (owners[n["god_anchor"]] ||= []) << node_owner
        end
        collect_iod_anchor_owners(n["children"] || [], computed, owners, node_owner) if n["children"]
        (n["sub_dials"] || []).each do |s|
          if s["god_anchor"]
            sub_owner = { "id" => s["id"], "name" => s["name"], "parent" => node_owner }
            (owners[s["god_anchor"]] ||= []) << sub_owner
          end
        end
      end
      owners
    end

    # Build a render-ready tree of the canonical GOD with linkage state for
    # every node. State values:
    #   linked     — at least one IOD board references this exact id.
    #   partial    — none / some children linked, with explicit off_dashboard
    #                metadata marking this as a partial fragmentation; OR
    #                a parent whose sub-dials have mixed link state.
    #   not-linked — no IOD reference, no off_dashboard entry. Pure absence.
    #   numb       — was tracked, transducer is dead. Currently unused; the
    #                schema supports it for parity with the prior off_dashboard
    #                taxonomy (status: numb).
    # never-cared maps to not-linked + an off_dashboard note ("never-cared" is
    # a *reason* for not-linked, not a separate state on the tree itself).
    #
    # NOTE on the unified tree (2026-04-23): god_tree.yml now has a single
    # top-level `themes:` array instead of the prior `bubble:` / `outside:`
    # split. Dials carry `bubble: true|false` and an optional `vantages:` list
    # so the demographic-vantage information (national-security, electorate,
    # rural, religious, gen-z, older-adults, immigrant, parents) is preserved
    # as a property of each node rather than as a structural prefix.
    def build_god_tree_render(god_data, anchor_owners, off_by_anchor)
      totals = { "total" => 0, "linked" => 0, "partial" => 0,
                 "not_linked" => 0, "numb" => 0,
                 "bubble" => 0, "outside_bubble" => 0 }

      walker = lambda do |nodes|
        (nodes || []).map do |node|
          children = walker.call(node["dials"])
          owners = anchor_owners[node["id"]] || []
          off    = off_by_anchor[node["id"]]

          state =
            if owners.any?
              if children.any? && children.any? { |c| c["state"] == "not-linked" } && children.any? { |c| c["state"] == "linked" }
                "partial"
              else
                "linked"
              end
            elsif off && off["status"] == "numb"
              "numb"
            elsif off && off["status"] == "partial"
              "partial"
            elsif children.any? && children.any? { |c| c["state"] == "linked" || c["state"] == "partial" }
              "partial"
            elsif off && off["status"] == "never-cared"
              "not-linked"
            else
              "not-linked"
            end

          totals["total"] += 1
          case state
          when "linked"     then totals["linked"]     += 1
          when "partial"    then totals["partial"]    += 1
          when "numb"       then totals["numb"]       += 1
          else                   totals["not_linked"] += 1
          end

          # Track bubble vs. outside-bubble counts at the dial level (themes
          # don't carry a `bubble:` field in the unified schema).
          if node.key?("bubble")
            if node["bubble"]
              totals["bubble"] += 1
            else
              totals["outside_bubble"] += 1
            end
          end

          {
            "id"           => node["id"],
            "name"         => node["name"],
            "summary"      => node["summary"],
            "state"        => state,
            "owners"       => owners,
            "off_metadata" => off,
            "bubble"       => node["bubble"],
            "vantages"     => node["vantages"] || [],
            "cross_themes" => node["cross_themes"] || [],
            "dials"        => children,
          }
        end
      end

      themes = walker.call(god_data["themes"])

      { "themes" => themes, "totals" => totals }
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
