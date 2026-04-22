---
title: Internal Okayness
permalink: /okayness/
layout: page
sitemap: false
---

<style>
  .okayness-tree { list-style: none; padding-left: 0; margin-top: 1.5rem; }
  .okayness-theme { margin: 0.5rem 0; padding: 0; }
  .okayness-theme > summary {
    list-style: none;                 /* hide default disclosure triangle */
    cursor: pointer;
    padding: 0.35rem 0;
  }
  .okayness-theme > summary::-webkit-details-marker { display: none; }
  .okayness-theme > summary::before {
    content: "▸";
    display: inline-block;
    width: 1em;
    margin-right: 0.15rem;
    color: #aaa;
    transition: transform 0.15s ease;
  }
  .okayness-theme[open] > summary::before { transform: rotate(90deg); }
  .okayness-children {
    list-style: none;
    padding-left: 1.75rem;
    border-left: 1px dashed #d8d8d2;
    margin: 0.25rem 0 0.75rem 0.7rem;
  }
  .okayness-row {
    display: flex; align-items: center; gap: 0.6rem;
    font-family: inherit;
  }
  .okayness-dial { flex-shrink: 0; vertical-align: middle; }
  .okayness-name { flex: 1; }
  .okayness-trend { font-size: 0.8rem; color: #888; }
  .okayness-trend.up { color: #2d7a3a; }
  .okayness-trend.down { color: #b03a36; }
  .okayness-meta { font-size: 0.7rem; color: #999; }
  .okayness-numb-flag { color: #b03a36; font-size: 0.75rem; font-weight: 600; margin-left: 0.4rem; }
  .okayness-legend { font-size: 0.85rem; color: #666; margin: 1rem 0; }
  .okayness-recent { font-size: 0.8rem; color: #555; margin-top: 0.35rem; padding-left: 1rem; border-left: 2px solid #f0e8d0; }
  .okayness-recent .rating { margin-bottom: 0.2rem; }
  .okayness-child { padding: 0.3rem 0; }
</style>

A subjective dashboard of how I'm feeling across the parts of my life that matter.
Each theme starts collapsed — click to expand and see the boards underneath.

<p class="okayness-meta">
  {{ site.data.okayness.total_ratings }} total ratings
  · last build {{ site.data.okayness.last_updated }}
</p>

<div class="okayness-tree">
{% for theme in site.data.okayness.tree.themes %}
  {% assign t = site.data.okayness.computed[theme.id] %}
  <details class="okayness-theme">
    <summary>
      <span class="okayness-row">
        {% include okayness-dial.html score=t.effective_score size=44 %}
        <strong class="okayness-name">{{ theme.name }}</strong>
        {% if t.trend %}
          <span class="okayness-trend {% if t.trend > 0 %}up{% elsif t.trend < 0 %}down{% endif %}">
            {% if t.trend > 0 %}+{% endif %}{{ t.trend }}
          </span>
        {% endif %}
      </span>
    </summary>
    {% if theme.children %}
    <ul class="okayness-children">
      {% for child in theme.children %}
        {% assign c = site.data.okayness.computed[child.id] %}
        <li class="okayness-child">
          <div class="okayness-row">
            {% include okayness-dial.html score=c.effective_score size=36 %}
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
  </details>
{% endfor %}
</div>

<p class="okayness-legend" style="display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap;">
  <span>Dial reference —</span>
  {% include okayness-dial.html score=7 size=44 %} <span>Great</span>
  {% include okayness-dial.html score=5 size=44 %} <span>Okay</span>
  {% include okayness-dial.html score=4 size=44 %} <span>Neutral</span>
  {% include okayness-dial.html score=3 size=44 %} <span>Not okay</span>
  {% include okayness-dial.html score=1 size=44 %} <span>Terrible</span>
  {% include okayness-dial.html score=0 size=44 %} <span>Numb</span>
</p>

<p class="okayness-legend">
  Scores use a 0–7 scale (7 Great → 0 Numb) and per-board EWMA with a tunable half-life.
  Parent themes blend their children's scores. Trend is the signed delta vs. 30 days ago.
</p>
