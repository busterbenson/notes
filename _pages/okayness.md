---
title: Internal Okayness
permalink: /okayness/
layout: page
sitemap: false
---

<style>
  /* ── Layout ─────────────────────────────────────────────────────────── */
  .ok-intro {
    color: #555; font-size: 0.95rem; line-height: 1.55;
    margin: 0 0 1.5rem 0;
  }
  .ok-pulse {
    display: flex; gap: 1.5rem; flex-wrap: wrap;
    padding: 0.6rem 0; margin-bottom: 1.75rem;
    border-top: 1px solid #ece8d8; border-bottom: 1px solid #ece8d8;
    font-size: 0.78rem; color: #888;
    text-transform: uppercase; letter-spacing: 0.07em;
  }
  .ok-pulse strong { color: #333; font-weight: 600; font-size: 0.92rem; text-transform: none; letter-spacing: 0; }

  .ok-grid {
    display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem; margin: 0;
  }
  @media (max-width: 640px) { .ok-grid { grid-template-columns: 1fr; } }

  /* ── Theme cards ───────────────────────────────────────────────────── */
  .ok-card {
    background: #fdfcf6;
    border: 1px solid #ece8d8;
    border-radius: 10px;
    padding: 0;
    margin: 0;
    transition: border-color 0.15s ease, background 0.15s ease, transform 0.1s ease;
    list-style: none;
  }
  .ok-card[open] { background: #faf8ef; border-color: #d8d2bc; }
  .ok-card:hover { border-color: #c8c1a8; }
  .ok-card > summary {
    list-style: none;
    display: flex; align-items: center; gap: 0.85rem;
    padding: 0.9rem 1rem;
    cursor: pointer;
    border-radius: 10px;
  }
  .ok-card > summary::-webkit-details-marker { display: none; }
  .ok-card > summary::after {
    content: "›";
    color: #b6ad8a; font-size: 1.4rem; line-height: 1;
    transition: transform 0.15s ease;
  }
  .ok-card[open] > summary::after { transform: rotate(90deg); }

  .ok-card-name { font-weight: 600; font-size: 1.05rem; flex: 1; color: #1a1a1a; }
  .ok-card-trend { font-size: 0.78rem; color: #999; font-variant-numeric: tabular-nums; }
  .ok-card-trend.up { color: #2d7a3a; }
  .ok-card-trend.down { color: #b03a36; }

  /* ── Boards inside a card ─────────────────────────────────────────── */
  .ok-boards {
    list-style: none; margin: 0; padding: 0 0.4rem 0.6rem 0.4rem;
    border-top: 1px dashed #e2dcc6;
  }
  .ok-board {
    display: flex; align-items: center; gap: 0.7rem;
    padding: 0.55rem 0.6rem;
    border-radius: 6px;
    transition: background 0.1s ease;
  }
  .ok-board:hover { background: #f6f1de; }
  .ok-board-info { flex: 1; min-width: 0; }
  .ok-board-name { font-size: 0.95rem; color: #2a2a2a; }
  .ok-board-meta { font-size: 0.7rem; color: #a59f88; margin-top: 0.1rem; }
  .ok-board-trend { font-size: 0.75rem; color: #999; font-variant-numeric: tabular-nums; flex-shrink: 0; }
  .ok-board-trend.up { color: #2d7a3a; }
  .ok-board-trend.down { color: #b03a36; }
  .ok-numb-flag { color: #a83834; font-size: 0.7rem; font-weight: 600; margin-left: 0.4rem; text-transform: uppercase; letter-spacing: 0.05em; }

  /* ── Recent ratings drawer (deepest level) ────────────────────────── */
  .ok-recent {
    grid-column: 1 / -1;
    font-size: 0.78rem; color: #6f6a55;
    margin-top: 0.25rem; padding: 0.4rem 0.7rem;
    background: #f8f4e2; border-radius: 4px;
  }
  .ok-recent-row { display: flex; gap: 0.6rem; padding: 0.1rem 0; }
  .ok-recent-row strong { color: #333; min-width: 1.5rem; }
  .ok-recent-row .at { color: #a59f88; min-width: 3rem; }
  .ok-recent-row .note { color: #6f6a55; font-style: italic; }
  details.ok-board-deep { display: contents; }
  details.ok-board-deep > summary { list-style: none; cursor: pointer; }
  details.ok-board-deep > summary::-webkit-details-marker { display: none; }

  /* ── Legend ───────────────────────────────────────────────────────── */
  .ok-legend {
    margin-top: 2.5rem; padding-top: 1.25rem; border-top: 1px solid #ece8d8;
    color: #888; font-size: 0.82rem;
  }
  .ok-legend-dials {
    display: flex; gap: 0.9rem; flex-wrap: wrap; align-items: center;
    margin: 0.75rem 0 1rem 0;
  }
  .ok-legend-dials > div {
    display: flex; flex-direction: column; align-items: center; gap: 0.1rem;
    color: #888; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em;
  }
  .ok-legend p { margin: 0.4rem 0; line-height: 1.55; }

  .okayness-dial { display: block; flex-shrink: 0; }
</style>

<p class="ok-intro">
  A subjective gauge of how I'm feeling, by area of life. I rate things directly
  when I check in. Each board's score is an exponentially-weighted moving average
  with its own half-life, so old feelings fade naturally and the dial moves at the
  pace each part of life actually moves at.
</p>

{%- assign rated_themes = "" | split: "" -%}
{%- for theme in site.data.okayness.tree.themes -%}
  {%- assign t = site.data.okayness.computed[theme.id] -%}
  {%- if t.effective_score -%}{%- assign rated_themes = rated_themes | push: t.effective_score -%}{%- endif -%}
{%- endfor -%}
{%- assign overall = nil -%}
{%- if rated_themes.size > 0 -%}
  {%- assign sum = 0 -%}
  {%- for s in rated_themes -%}{%- assign sum = sum | plus: s -%}{%- endfor -%}
  {%- assign overall = sum | divided_by: rated_themes.size -%}
{%- endif -%}

<div class="ok-pulse">
  <div>Overall <strong>{% if overall %}{{ overall | round: 1 }}{% else %}—{% endif %}</strong></div>
  <div>Themes <strong>{{ site.data.okayness.tree.themes.size }}</strong></div>
  <div>Ratings <strong>{{ site.data.okayness.total_ratings }}</strong></div>
  <div>Updated <strong>{{ site.data.okayness.last_updated | date: "%b %-d, %Y" }}</strong></div>
</div>

<div class="ok-grid">
{% for theme in site.data.okayness.tree.themes %}
  {% assign t = site.data.okayness.computed[theme.id] %}
  <details class="ok-card">
    <summary>
      {% include okayness-dial.html score=t.effective_score size=52 %}
      <span class="ok-card-name">{{ theme.name }}</span>
      {% if t.trend and t.trend != 0 %}
        <span class="ok-card-trend {% if t.trend > 0 %}up{% elsif t.trend < 0 %}down{% endif %}">
          {% if t.trend > 0 %}+{% endif %}{{ t.trend }}
        </span>
      {% endif %}
    </summary>
    {% if theme.children %}
    <ul class="ok-boards">
      {% for child in theme.children %}
        {% assign c = site.data.okayness.computed[child.id] %}
        <li>
          <details class="ok-board-deep">
            <summary class="ok-board">
              {% include okayness-dial.html score=c.effective_score size=36 %}
              <div class="ok-board-info">
                <div class="ok-board-name">
                  {{ child.name }}
                  {% if c.numb_streak_days > 0 %}<span class="ok-numb-flag">numb {{ c.numb_streak_days }}d</span>{% endif %}
                </div>
                <div class="ok-board-meta">
                  {{ c.leaf_count }} rating{% if c.leaf_count != 1 %}s{% endif %} · half-life {{ c.resilience_days }}d
                </div>
              </div>
              {% if c.trend and c.trend != 0 %}
                <span class="ok-board-trend {% if c.trend > 0 %}up{% elsif c.trend < 0 %}down{% endif %}">
                  {% if c.trend > 0 %}+{% endif %}{{ c.trend }}
                </span>
              {% endif %}
            </summary>
            {% if c.recent and c.recent.size > 0 %}
              <div class="ok-recent">
                {% for r in c.recent reversed %}
                  {% if forloop.index <= 6 %}
                    <div class="ok-recent-row">
                      <strong>{{ r.score }}</strong>
                      <span class="at">{{ r.at | date: "%b %-d" }}</span>
                      {% if r.note %}<span class="note">{{ r.note }}</span>{% endif %}
                    </div>
                  {% endif %}
                {% endfor %}
              </div>
            {% endif %}
          </details>
        </li>
      {% endfor %}
    </ul>
    {% endif %}
  </details>
{% endfor %}
</div>

<div class="ok-legend">
  <p><strong>How to read a dial.</strong> The needle's angle on the arc is the score. Right is good (greens), left is bad (reds), straight up is neutral. Numb is its own thing — needle pointed straight down at the dark dot, meaning <em>burnt out, can't feel</em>.</p>
  <div class="ok-legend-dials">
    <div>{% include okayness-dial.html score=7 size=44 %}<span>Great</span></div>
    <div>{% include okayness-dial.html score=6 size=44 %}<span>Good</span></div>
    <div>{% include okayness-dial.html score=5 size=44 %}<span>Okay</span></div>
    <div>{% include okayness-dial.html score=4 size=44 %}<span>Neutral</span></div>
    <div>{% include okayness-dial.html score=3 size=44 %}<span>Not okay</span></div>
    <div>{% include okayness-dial.html score=2 size=44 %}<span>Bad</span></div>
    <div>{% include okayness-dial.html score=1 size=44 %}<span>Terrible</span></div>
    <div>{% include okayness-dial.html score=0 size=44 %}<span>Numb</span></div>
  </div>
  <p><strong>How the math works.</strong> Each board has its own half-life — how long it takes for an old rating to count half as much. Body and relationships move on a 14-day half-life; bigger structural things (Therapy, Spirituality, World) on 60. Parent themes blend their children. Trend is the score now minus the score 30 days ago.</p>
  <p><strong>About this page.</strong> Subjective and just for me. Open and unlinked from the homepage. Boards and ratings live in <code>_data/okayness/</code> in the site repo.</p>
</div>
