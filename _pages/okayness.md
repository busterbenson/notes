---
title: Internal Okayness
permalink: /okayness/
layout: page
sitemap: false
---

<style>
  .okayness-tree { list-style: none; padding-left: 0; margin-top: 1.5rem; }
  .okayness-tree ul { list-style: none; padding-left: 1.25rem; border-left: 1px dashed #d8d8d2; margin-left: 0.5rem; }
  .okayness-row {
    display: flex; align-items: baseline; gap: 0.6rem;
    padding: 0.35rem 0; font-family: inherit;
  }
  .okayness-name { flex: 1; }
  .okayness-score { font-variant-numeric: tabular-nums; font-weight: 600; min-width: 2.5rem; text-align: right; }
  .okayness-band {
    font-size: 0.75rem; padding: 1px 6px; border-radius: 10px;
    text-transform: uppercase; letter-spacing: 0.04em; color: #2a2a2a;
  }
  .band-great    { background: #6fcf97; }
  .band-good     { background: #9bd5a8; }
  .band-okay     { background: #c8e3b8; }
  .band-neutral  { background: #e3e3d0; }
  .band-not-okay { background: #f3d6a3; }
  .band-bad      { background: #ef9b80; }
  .band-terrible { background: #d96460; color: white; }
  .band-numb     { background: #888; color: white; }
  .band-none     { background: #f4f4ee; color: #aaa; }
  .okayness-trend { font-size: 0.8rem; color: #888; }
  .okayness-trend.up { color: #2d7a3a; }
  .okayness-trend.down { color: #b03a36; }
  .okayness-meta { font-size: 0.7rem; color: #999; }
  .okayness-numb-flag { color: #b03a36; font-size: 0.75rem; font-weight: 600; }
  .okayness-legend { font-size: 0.85rem; color: #666; margin: 1rem 0; }
  .okayness-recent { font-size: 0.8rem; color: #555; margin-top: 0.5rem; padding-left: 1rem; border-left: 2px solid #f0e8d0; }
  .okayness-recent .rating { margin-bottom: 0.2rem; }
</style>

A subjective dashboard of how I'm feeling across the parts of my life that matter.
Ratings are mine, set deliberately. Each board has an EWMA with a tunable half-life
(shown in days as `hl=N` next to the name). Parent boards blend their children's
scores. The 0–7 scale runs **7 Great → 6 Good → 5 Okay → 4 Neutral → 3 Not Okay →
2 Bad → 1 Terrible → 0 Numb**.

<p class="okayness-meta">
  {{ site.data.okayness.total_ratings }} total ratings
  · last build {{ site.data.okayness.last_updated }}
</p>

<ul class="okayness-tree">
{% for theme in site.data.okayness.tree.themes %}
  {% assign t = site.data.okayness.computed[theme.id] %}
  <li>
    <div class="okayness-row">
      <strong class="okayness-name">{{ theme.name }}</strong>
      {% if t.trend %}
        <span class="okayness-trend {% if t.trend > 0 %}up{% elsif t.trend < 0 %}down{% endif %}">
          {% if t.trend > 0 %}+{% endif %}{{ t.trend }}
        </span>
      {% endif %}
      <span class="okayness-score">{{ t.effective_score | default: "—" }}</span>
      <span class="okayness-band band-{{ t.effective_band }}">{{ t.effective_band | replace: "-", " " }}</span>
    </div>
    {% if theme.children %}
    <ul>
      {% for child in theme.children %}
        {% assign c = site.data.okayness.computed[child.id] %}
        <li>
          <div class="okayness-row">
            <span class="okayness-name">
              {{ child.name }}
              <span class="okayness-meta">hl={{ c.resilience_days }}d · {{ c.leaf_count }} ratings</span>
              {% if c.numb_streak_days > 0 %}
                <span class="okayness-numb-flag">numb ×{{ c.numb_streak_days }}d</span>
              {% endif %}
            </span>
            {% if c.trend %}
              <span class="okayness-trend {% if c.trend > 0 %}up{% elsif c.trend < 0 %}down{% endif %}">
                {% if c.trend > 0 %}+{% endif %}{{ c.trend }}
              </span>
            {% endif %}
            <span class="okayness-score">{{ c.effective_score | default: "—" }}</span>
            <span class="okayness-band band-{{ c.effective_band }}">{{ c.effective_band | replace: "-", " " }}</span>
          </div>
          {% if c.recent and c.recent.size > 0 %}
            <div class="okayness-recent">
              {% for r in c.recent reversed %}
                {% if forloop.index <= 5 %}
                  <div class="rating">
                    <strong>{{ r.score }}</strong>
                    · {{ r.at | date: "%b %d" }}
                    {% if r.note %}— <em>{{ r.note }}</em>{% endif %}
                  </div>
                {% endif %}
              {% endfor %}
            </div>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
    {% endif %}
  </li>
{% endfor %}
</ul>

<p class="okayness-legend">
  Bands: 6.5–7 great · 5.5–6.5 good · 4.5–5.5 okay · 3.5–4.5 neutral ·
  2.5–3.5 not okay · 1.5–2.5 bad · 0.5–1.5 terrible · 0–0.5 numb. The number is the
  exponentially-weighted moving average; trend is current minus 30-days-ago.
</p>
