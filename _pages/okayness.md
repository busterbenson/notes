---
title: Internal Okayness
permalink: /okayness/
layout: page
sitemap: false
---

<!-- build-probe: 1777256439 (verifying Ruby 4 Netlify deploy) -->

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

  /* ── GOD-link badge ───────────────────────────────────────────────── */
  /* A small dot next to a board name signals "this IOD board links to
     a node in the canonical GOD tree." Hover/tap reveals which one. */
  .ok-god-badge {
    display: inline-block;
    width: 0.5rem; height: 0.5rem;
    border-radius: 50%;
    background: #b6ad8a;
    margin-left: 0.4rem;
    vertical-align: 1px;
    cursor: help;
    transition: background 0.1s ease;
  }
  .ok-god-badge:hover { background: #8a8470; }

  /* ── Full GOD collapsible tree ────────────────────────────────────── */
  /* This is the index/map view of the entire canonical GOD, with linkage
     state at every node. Visually QUIETER than the dial widgets above —
     bulleted, monospace-friendly, no measurements. The actual measurements
     live in the dials; this view is the absence-and-presence pattern. */
  .ok-god-section {
    margin-top: 2.25rem;
    padding-top: 1.25rem;
    border-top: 1px dashed #d8d2bc;
  }
  .ok-god-header {
    display: flex; align-items: baseline; justify-content: space-between;
    flex-wrap: wrap; gap: 0.6rem;
    margin-bottom: 0.4rem;
  }
  .ok-god-header h2 {
    font-size: 0.95rem; font-weight: 600; color: #6f6a55;
    margin: 0; letter-spacing: 0.02em;
  }
  .ok-god-intro {
    color: #8a8470; font-size: 0.82rem; line-height: 1.55;
    margin: 0 0 0.6rem 0; max-width: 62ch;
  }
  .ok-god-coverage {
    font-size: 0.78rem; color: #8a8470; font-style: italic;
    margin: 0 0 1rem 0;
  }
  .ok-god-coverage strong { color: #6f6a55; font-style: normal; }
  .ok-god-coverage .swatch {
    display: inline-block; width: 0.55rem; height: 0.55rem;
    border-radius: 50%; vertical-align: 1px;
    margin: 0 0.15rem 0 0.4rem;
  }

  .god-tree, .god-tree ul {
    list-style: none; margin: 0; padding: 0;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.82rem;
  }
  .god-tree { line-height: 1.55; }
  .god-tree ul { padding-left: 1.25rem; border-left: 1px dotted #e2dcc6; margin-left: 0.45rem; }

  .god-umbrella { margin-top: 0.5rem; }
  .god-umbrella > summary {
    list-style: none; cursor: pointer;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.85rem; font-weight: 600;
    color: #6f6a55; text-transform: uppercase; letter-spacing: 0.07em;
    padding: 0.35rem 0;
  }
  .god-umbrella > summary::-webkit-details-marker { display: none; }
  .god-umbrella > summary::before {
    content: "▸"; display: inline-block; width: 1rem;
    color: #b6ad8a; transition: transform 0.1s ease;
  }
  .god-umbrella[open] > summary::before { content: "▾"; }

  .god-node { margin: 0.05rem 0; }
  .god-node > summary, .god-leaf {
    list-style: none; cursor: pointer;
    display: flex; align-items: baseline; gap: 0.45rem;
    padding: 0.1rem 0;
    color: #4a4538;
  }
  .god-leaf { cursor: default; }
  .god-node > summary::-webkit-details-marker { display: none; }
  .god-node > summary::before {
    content: "▸"; display: inline-block; width: 0.9rem;
    color: #b6ad8a; flex-shrink: 0;
  }
  .god-node[open] > summary::before { content: "▾"; }
  .god-leaf::before {
    content: "·"; display: inline-block; width: 0.9rem;
    color: #c8c1a8; flex-shrink: 0; text-align: center;
  }

  .god-marker {
    display: inline-block; flex-shrink: 0;
    width: 0.8rem; text-align: center;
    font-weight: 600; line-height: 1;
  }
  .god-marker.linked     { color: #2d7a3a; }   /* filled check */
  .god-marker.partial    { color: #b07c2d; }   /* half-state   */
  .god-marker.not-linked { color: #b6ad8a; }   /* empty        */
  .god-marker.numb       { color: #6e5a4f; }   /* dead-dot     */

  .god-name { color: #2a2a2a; }
  .god-node[data-state="not-linked"] > summary > .god-name,
  .god-leaf[data-state="not-linked"] > .god-name {
    color: #8a8470;
  }
  .god-node[data-state="numb"] > summary > .god-name,
  .god-leaf[data-state="numb"] > .god-name {
    color: #6e5a4f; font-style: italic;
  }

  .god-id {
    color: #b6ad8a; font-size: 0.7rem;
    margin-left: 0.3rem;
  }
  .god-link-into {
    color: #6f6a55; font-size: 0.72rem;
    margin-left: 0.5rem;
  }
  .god-link-into a { color: #2d7a3a; text-decoration: none; border-bottom: 1px dotted #b8d4be; }
  .god-link-into a:hover { border-bottom-style: solid; }

  .god-detail {
    margin: 0.2rem 0 0.4rem 1.85rem;
    padding: 0.3rem 0.55rem;
    background: #f6f1de;
    border-radius: 4px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 0.78rem; color: #6f6a55; line-height: 1.5;
  }
  .god-detail .god-summary { color: #4a4538; }
  .god-detail .god-note {
    margin-top: 0.25rem; font-style: italic;
  }
  .god-detail .god-status-tag {
    display: inline-block;
    font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.07em;
    padding: 0.05rem 0.35rem; border-radius: 3px;
    margin-right: 0.3rem; vertical-align: 1px;
    font-weight: 600;
    background: #ece8d8; color: #8a8470;
  }
  .god-detail .god-status-tag.partial     { background: #e3ddc4; color: #6f6a3a; }
  .god-detail .god-status-tag.numb        { background: #e0d4cc; color: #5a4a42; }
  .god-detail .god-status-tag.never-cared { background: #ece8d8; color: #8a8470; }

  /* ── Bubble / vantage flags on GOD nodes (unified tree) ───────────── */
  /* Each dial in the unified GOD tree carries either an "in bubble" flag
     (Buster's current radar) or a "salient to: <vantage>" flag (a
     demographic constituency for which the dial is especially salient).
     Quiet typography — these are meta-data labels, not measurements. */
  .god-flag {
    display: inline-block;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.06em;
    padding: 0.05rem 0.35rem; border-radius: 3px;
    margin-left: 0.35rem; vertical-align: 1px;
    font-weight: 500;
    background: transparent;
  }
  .god-flag.bubble  { color: #5a7a3a; background: #eef3e0; }
  .god-flag.vantage { color: #6f5a3a; background: #f3ecd8; }
  .god-flag.outside { color: #8a8470; background: #ece8d8; }
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
                  {% if c.god_anchor %}<span class="ok-god-badge" title="Linked to GOD: {{ c.god_anchor }}"></span>{% endif %}
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

{% if site.data.okayness.god_render %}
<section class="ok-god-section">
  <div class="ok-god-header">
    <h2>Global dashboard projection</h2>
    {% assign tot = site.data.okayness.god_render.totals %}
    <span class="ok-god-coverage">{{ tot.total }} GOD nodes</span>
  </div>
  <p class="ok-god-intro">
    The full <a href="https://github.com/busterbenson/chalantbot-obsidian/blob/main/Wiki/pages/global-okayness-dashboard.md">canonical GOD tree</a>
    rendered as an index — one unified hierarchy organized by theme. Every dial carries
    a flag: <span class="god-flag bubble">in bubble</span> if it's on Buster's current radar,
    or <span class="god-flag vantage">salient to: …</span> for the demographic vantages
    (national-security analyst, median voter, rural America, religious communities, Gen Z,
    older adults, immigrants, parents) where the dial is especially loud. The hierarchy
    here is the world's; the hierarchy above is Buster's. The pattern of presence and
    absence — at every level — is the salience function, made legible.
  </p>
  <p class="ok-god-coverage">
    <span class="god-marker linked">●</span> <strong>{{ tot.linked }}</strong> linked
    <span class="god-marker partial">◐</span> <strong>{{ tot.partial }}</strong> partial
    <span class="god-marker not-linked">○</span> <strong>{{ tot.not_linked }}</strong> not linked
    {% if tot.numb > 0 %}<span class="god-marker numb">●</span> <strong>{{ tot.numb }}</strong> numb{% endif %}
    &middot; <strong>{{ tot.bubble }}</strong> in bubble, <strong>{{ tot.outside_bubble }}</strong> outside
  </p>

  {%- assign render = site.data.okayness.god_render -%}

  <ul class="god-tree">
    {% for theme in render.themes %}{% include okayness-god-node.html node=theme %}{% endfor %}
  </ul>
</section>
{% endif %}

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
  <p><strong>Hierarchy is salience.</strong> A board near the top of the dashboard is top of mind; a board nested inside a theme is less so. The ordering isn't an organizational convenience — it's the projection function from the world's dashboard onto the parts of it I've actually installed.</p>
  <p><strong>Global dashboard projection.</strong> The collapsible tree at the bottom is the entire <a href="https://github.com/busterbenson/chalantbot-obsidian/blob/main/Wiki/pages/global-okayness-dashboard.md">canonical GOD</a> as a single theme-organized hierarchy. Each node is marked <span class="god-marker linked">●</span> linked (an IOD board points at it), <span class="god-marker partial">◐</span> partial (some children linked, some not, or absorbed by a nearby IOD board), <span class="god-marker not-linked">○</span> not linked (no IOD coupling — most often a vantage built for other bells), or <span class="god-marker numb">●</span> numb (was tracked, transducer went dead). Each dial also carries a flag: <span class="god-flag bubble">in bubble</span> for dials on Buster's current radar, or <span class="god-flag vantage">salient to: &lt;vantage&gt;</span> for dials whose primary audience is a specific demographic constituency. Expand a node to see what links into it, the one-line summary from the wiki, and any partial-fragmentation notes.</p>
  <p><strong>About this page.</strong> Subjective and just for me. Open and unlinked from the homepage. Boards and ratings live in <code>_data/okayness/</code> in the site repo.</p>
</div>
