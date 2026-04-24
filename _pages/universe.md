---
title: The Universe at a Glance
permalink: /universe/
layout: fullscreen
sitemap: false
---

<style>
  body { background: #faf8f0; }
  #fullscreen { padding: 1.5rem 1.5rem 3rem; max-width: none; }
  .uni-page-title { font-family: "Open Sans", sans-serif; font-weight: 700; font-size: 1.6rem; margin: 0 0 0.4rem 0; color: #1a1a1a; }
  .uni-intro { color: #555; font-size: 0.95rem; line-height: 1.55; max-width: 70ch; margin: 0 0 1.5rem 0; }
  .uni-charts { display: grid; grid-template-columns: 1fr; gap: 1.5rem; margin-top: 1rem; }
  @media (min-width: 1200px) { .uni-charts { grid-template-columns: 1fr 1fr; } }

  .uni-chart { background: #fdfcf6; border: 1px solid #ece8d8; border-radius: 12px; padding: 1.25rem; }
  .uni-chart-header { display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 0.6rem; }
  .uni-chart-title { font-weight: 600; font-size: 1.05rem; color: #1a1a1a; margin: 0; }
  .uni-chart-subtitle { color: #888; font-size: 0.8rem; }

  .uni-canvas { width: 100%; aspect-ratio: 1.4 / 1; min-height: 480px; }

  .uni-legend { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.75rem; }
  .uni-chip {
    display: inline-flex; align-items: center; gap: 0.35rem;
    padding: 0.2rem 0.6rem; border-radius: 999px;
    font-size: 0.78rem; cursor: pointer;
    background: #faf8ef; border: 1px solid #d8d2bc; color: #2a2a2a;
    transition: opacity 0.12s ease;
  }
  .uni-chip[data-on="false"] { opacity: 0.4; text-decoration: line-through; }
  .uni-chip[data-on="false"] .uni-chip-dot { background: #ccc !important; }
  .uni-chip-dot { width: 0.55rem; height: 0.55rem; border-radius: 50%; }

  /* Cross-chart linking — when one object is hovered, the others fade
     across both panels so the eye can find its counterpart. */
  .uni-dimmed { opacity: 0.18; transition: opacity 0.18s ease; }
  .uni-spot   { opacity: 1.0;  transition: opacity 0.18s ease; }
  .uni-spot circle, .uni-spot rect, .uni-spot path {
    stroke: #1a1a1a; stroke-width: 2;
  }

  /* Hovered label pops out of crowded clusters: forced visible,
     larger, with a soft pill behind it via paint-order so the text
     reads on top of any overlap. */
  .uni-label-dimmed { opacity: 0.12 !important; transition: opacity 0.18s ease; }
  .uni-label-spot {
    opacity: 1 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    fill: #1a1a1a !important;
    paint-order: stroke fill;
    stroke: #fffceb;
    stroke-width: 5px;
    stroke-linejoin: round;
  }

  /* Tour mode UI */
  .uni-tour-bar {
    display: flex; gap: 0.5rem; align-items: center;
    margin: 0.5rem 0 1rem; flex-wrap: wrap;
  }
  .uni-tour-btn {
    background: #fdfcf6; border: 1px solid #cdc8b6; border-radius: 999px;
    padding: 0.35rem 0.95rem; font-size: 0.85rem; cursor: pointer;
    color: #2a2a2a; transition: background 0.15s ease, border-color 0.15s ease;
    display: inline-flex; align-items: center; gap: 0.35rem;
  }
  .uni-tour-btn:hover { background: #f3eeda; border-color: #b8b194; }
  .uni-tour-btn.primary { background: #2a2a2a; color: #fffceb; border-color: #2a2a2a; }
  .uni-tour-btn.primary:hover { background: #1a1a1a; }
  .uni-tour-controls { display: none; gap: 0.4rem; align-items: center; }
  .uni-tour-card {
    display: none; position: fixed; bottom: 1.25rem; left: 50%;
    transform: translateX(-50%);
    background: rgba(28, 24, 16, 0.94); color: #f5f0df;
    padding: 0.85rem 1.25rem; border-radius: 10px;
    max-width: 540px; min-width: 320px; z-index: 900;
    box-shadow: 0 8px 28px rgba(0,0,0,0.35);
    line-height: 1.5;
  }
  .uni-tour-counter { color: #c8b893; font-size: 0.72rem; letter-spacing: 0.07em; text-transform: uppercase; }
  .uni-tour-name { font-size: 1.05rem; font-weight: 700; color: #ffe9b8; margin: 0.25rem 0; }
  .uni-tour-story { font-size: 0.88rem; }

  .uni-tooltip {
    position: absolute; pointer-events: none;
    background: rgba(28, 24, 16, 0.92); color: #f5f0df;
    padding: 0.5rem 0.7rem; border-radius: 6px;
    font-size: 0.78rem; max-width: 280px; line-height: 1.45;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    transition: opacity 0.1s ease;
    opacity: 0; z-index: 1000;
  }
  .uni-tooltip strong { color: #ffe9b8; font-weight: 600; }
  .uni-tooltip .meta { color: #c8b893; font-variant-numeric: tabular-nums; font-size: 0.74rem; margin-top: 0.25rem; }

  .uni-footer { margin-top: 2.5rem; padding-top: 1.25rem; border-top: 1px solid #ece8d8; color: #888; font-size: 0.82rem; }
  .uni-footer details { margin-top: 0.5rem; }
  .uni-footer summary { cursor: pointer; color: #555; }
  .uni-footer ul { padding-left: 1.5rem; margin: 0.5rem 0; }
  .uni-footer li { margin: 0.2rem 0; line-height: 1.45; }
</style>

<h1 class="uni-page-title">The Universe at a Glance</h1>
<p class="uni-intro">
  Two paired interactive charts of <strong>everything that physically exists</strong>.
  The left chart is the Carr–Rees mass-radius diagram — the geometry of what's
  possible at all. The right chart is its temporal companion — when each
  density regime got populated, and how the universe itself has moved through
  them since the Big Bang. Hover any object to highlight it on both charts,
  or take the tour for a guided walk from observable universe down to electron.
</p>

<div class="uni-tour-bar">
  <button id="uni-tour-button" class="uni-tour-btn primary">▶ Take the tour</button>
  <div id="uni-tour-controls" class="uni-tour-controls">
    <button id="uni-tour-prev" class="uni-tour-btn">◀ Prev</button>
    <button id="uni-tour-next" class="uni-tour-btn">Next ▶</button>
    <button id="uni-tour-stop" class="uni-tour-btn">Stop</button>
    <span style="color:#888;font-size:0.78rem;">← → arrows · Esc to stop</span>
  </div>
</div>

<div class="uni-charts">

  <div class="uni-chart">
    <div class="uni-chart-header">
      <h2 class="uni-chart-title">Mass × Size</h2>
      <span class="uni-chart-subtitle">log-log, proton-normalized · after Ianni et al. 2022</span>
    </div>
    <div id="chart-mass-size" class="uni-canvas"></div>
    <div class="uni-legend" id="legend-mass-size"></div>
  </div>

  <div class="uni-chart">
    <div class="uni-chart-header">
      <h2 class="uni-chart-title">Density × Time</h2>
      <span class="uni-chart-subtitle">log density · symmetric-log time from now (0 = present)</span>
    </div>
    <div id="chart-density-time" class="uni-canvas"></div>
    <div class="uni-legend" id="legend-density-time"></div>
  </div>

</div>

<div id="uni-tooltip" class="uni-tooltip"></div>
<div id="uni-tour-card" class="uni-tour-card"></div>

<div class="uni-footer">
  <p>
    Carr–Rees layout follows Ianni, Mannarelli & Rossi (2022) Figure 2,
    "A new approach to dark matter from the mass–radius diagram of the
    Universe", <em>Results in Physics</em> 38 105544.
    Data points sourced from NASA NSSDC fact sheets, the Particle Data Group
    (2024), Planck 2018 cosmological parameters, the Event Horizon Telescope
    collaboration, and a few specialty references for biological and
    cosmological structures.
  </p>
  <details>
    <summary>Full source list</summary>
    <ul>
      {% for src in site.data.universe.sources.sources %}
        <li><strong>{{ src.short }}</strong> — {{ src.citation }}</li>
      {% endfor %}
    </ul>
  </details>
</div>

<script>
  // Pass the data into JS-land via a JSON island.
  window.UniverseData = {
    objects: {{ site.data.universe.objects.objects | jsonify }},
    sources: {{ site.data.universe.sources.sources | jsonify }}
  };
</script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="/assets/js/universe/main.js?v=14"></script>
