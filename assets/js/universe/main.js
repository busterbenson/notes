/* /universe/ — paired interactive charts.
 *
 * Chart 1 — Mass × Size (Carr-Rees, proton-normalized log-log).
 * Chart 2 — Density × Time (symmetric-log time axis, log density y).
 *
 * v0.5 — scaffolding plus first cut of both charts. Polishing happens
 * across follow-up iterations: animated transitions, label fade-on-zoom,
 * touch-friendly pinch/pan, "tour" mode, cross-chart linking.
 *
 * Data is injected via window.UniverseData.{objects, sources} from the
 * Liquid template.
 */

(function () {
  "use strict";

  // ── Constants ────────────────────────────────────────────────────────
  const M_PROTON_KG = 1.6726219e-27;
  const LAMBDA_PROTON_M = 1.32141e-15;
  const PLANCK_MASS_KG = 2.176434e-8;
  const PLANCK_LENGTH_M = 1.616255e-35;
  const G_NEWTON = 6.674e-11;
  const C_LIGHT = 2.998e8;
  const HBAR = 1.0546e-34;
  const SECONDS_PER_YEAR = 3.15576e7;

  const UNIVERSE_AGE_YEARS = 1.38e10;
  const UNIVERSE_AGE_S = UNIVERSE_AGE_YEARS * SECONDS_PER_YEAR; // ≈ 4.355e17 s
  const PLANCK_TIME_S = 5.391e-44;

  const BAND_COLORS = {
    nuclear:   "#b03a36",
    atomic:    "#3fa648",
    "dark-matter": "#a55ec2",
    radiation: "#2d6db0",
    planck:    "#6b4f3a",
    quantum:   "#7b8fa1",
  };

  const BAND_LABELS = {
    nuclear:   "Nuclear density",
    atomic:    "Atomic density",
    "dark-matter": "Dark-matter density",
    radiation: "Radiation",
    planck:    "Planck",
    quantum:   "Quantum",
  };

  const data = window.UniverseData;
  if (!data) {
    console.error("UniverseData missing");
    return;
  }

  // Normalize the YAML-derived data — convert any numeric strings and
  // pre-compute derived values once.
  data.objects.forEach(o => {
    o.mass_kg = +o.mass_kg;
    o.radius_m = +o.radius_m;
    o.density_kg_m3 = +o.density_kg_m3;
    o.x_log_r = Math.log10(o.radius_m / LAMBDA_PROTON_M);
    o.y_log_m = Math.log10(o.mass_kg / M_PROTON_KG);
    if (o.formation) {
      if (o.formation.time_ya != null) {
        o.formation.time_seconds_ago = o.formation.time_ya * SECONDS_PER_YEAR;
        if (o.formation.time_after_bb_s == null) {
          o.formation.time_after_bb_s = Math.max(
            PLANCK_TIME_S,
            UNIVERSE_AGE_S - o.formation.time_seconds_ago
          );
        }
      }
    }
    o.prominence = labelProminence(o);
  });

  // Label-prominence tier for zoom-aware visibility on Chart 1.
  // 1 = always visible, 2 = visible at k≥2, 3 = k≥4, 4 = k≥8.
  // Tuned so the default view shows ~12 well-known objects without
  // crowding, and zooming in reveals the rest by tier.
  function labelProminence(o) {
    const headline = new Set([
      "observable-universe", "milky-way", "andromeda", "laniakea",
      "sun", "earth", "moon", "jupiter",
      "sgr-a", "m87-smbh", "crab-pulsar", "stellar-bh",
      "human", "blue-whale",
      "proton", "electron", "eukaryotic-cell",
    ]);
    if (headline.has(o.id)) return 1;
    if (o.category === "planet" || o.category === "star") return 2;
    if (o.category === "galaxy" || o.category === "cluster") return 2;
    if (o.category === "compact-object" || o.category === "structure") return 2;
    if (o.category === "particle" || o.category === "atom") return 3;
    return 3;
  }

  function visibleAtZoom(prominence, k) {
    if (k >= 8) return true;
    if (k >= 4) return prominence <= 3;
    if (k >= 2) return prominence <= 2;
    return prominence <= 1;
  }

  // ── Tooltip ──────────────────────────────────────────────────────────
  const tooltip = d3.select("#uni-tooltip");

  function showTooltip(event, obj) {
    const lines = [
      `<strong>${obj.name}</strong>`,
      `<div class="meta">${formatScientific(obj.mass_kg, "kg")} · ${formatScientific(obj.radius_m, "m")} · ${formatScientific(obj.density_kg_m3, "kg/m³")}</div>`,
      obj.blurb ? `<div style="margin-top:0.35rem;">${obj.blurb}</div>` : "",
    ].join("");
    tooltip
      .html(lines)
      .style("left", (event.clientX + 14) + "px")
      .style("top", (event.clientY + 14) + "px")
      .style("opacity", 1);
  }
  function moveTooltip(event) {
    tooltip
      .style("left", (event.clientX + 14) + "px")
      .style("top", (event.clientY + 14) + "px");
  }
  function hideTooltip() {
    tooltip.style("opacity", 0);
  }

  function formatScientific(n, unit) {
    if (n === 0 || !isFinite(n)) return `0 ${unit}`;
    const log = Math.log10(Math.abs(n));
    const exp = Math.floor(log);
    const mantissa = n / Math.pow(10, exp);
    const m = mantissa.toFixed(2);
    return `${m}×10^${exp} ${unit}`;
  }

  // ── Shared color/shape helpers ───────────────────────────────────────
  function shapePath(shape, size) {
    // Returns a d-attribute path or just renders via SVG primitives below.
    // Used for the legend; the chart renders shapes inline.
    return null;
  }

  function renderShape(g, obj, size) {
    const c = obj.color || BAND_COLORS[obj.color_band] || "#222";
    if (obj.shape === "circle") {
      g.append("circle").attr("r", size).attr("fill", c);
    } else if (obj.shape === "square") {
      g.append("rect").attr("x", -size).attr("y", -size)
       .attr("width", size * 2).attr("height", size * 2).attr("fill", c);
    } else if (obj.shape === "diamond") {
      g.append("rect")
       .attr("x", -size).attr("y", -size)
       .attr("width", size * 2).attr("height", size * 2)
       .attr("fill", c)
       .attr("transform", "rotate(45)");
    } else if (obj.shape === "cross") {
      g.append("path")
       .attr("d", `M${-size},0 L${size},0 M0,${-size} L0,${size}`)
       .attr("stroke", c).attr("stroke-width", 2).attr("fill", "none");
    } else if (obj.shape === "asterisk") {
      // Six-pointed asterisk
      const pts = [];
      for (let i = 0; i < 6; i++) {
        const a = (i * Math.PI) / 6 * 2;
        pts.push(`M0,0 L${Math.sin(a) * size},${-Math.cos(a) * size}`);
      }
      g.append("path").attr("d", pts.join(" "))
       .attr("stroke", c).attr("stroke-width", 1.6).attr("fill", "none");
    } else {
      g.append("circle").attr("r", size).attr("fill", c);
    }
  }

  // ─────────────────────────────────────────────────────────────────────
  // CHART 1 — Mass × Size (Carr-Rees)
  // ─────────────────────────────────────────────────────────────────────
  function buildMassSizeChart() {
    const containerEl = document.getElementById("chart-mass-size");
    if (!containerEl) return;
    const W = containerEl.clientWidth;
    const H = containerEl.clientHeight;
    const margin = { top: 20, right: 20, bottom: 50, left: 60 };
    const innerW = W - margin.left - margin.right;
    const innerH = H - margin.top - margin.bottom;

    const svg = d3.select(containerEl).append("svg")
      .attr("viewBox", `0 0 ${W} ${H}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .style("width", "100%").style("height", "100%");

    // Domains: Planck-normalized log axes are wide, but we plot in
    // proton-normalized to match Ianni Fig. 2.
    const xDomain = [-22, 50]; // log10(r/λ_p)
    const yDomain = [-15, 85]; // log10(m/m_p)

    const xScale = d3.scaleLinear().domain(xDomain).range([0, innerW]);
    const yScale = d3.scaleLinear().domain(yDomain).range([innerH, 0]);

    const root = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    root.append("rect")
      .attr("width", innerW).attr("height", innerH)
      .attr("fill", "#fdfcf6").attr("stroke", "#cdc8b6");

    // Clip path so zoomed/panned content can't escape the plot area.
    const clipId = "uni-clip-mass-size";
    svg.append("defs").append("clipPath").attr("id", clipId)
      .append("rect").attr("width", innerW).attr("height", innerH);

    // The "view" group holds everything that pans/zooms — gridlines,
    // boundary lines, density diagonals, points, labels. Axes live
    // outside it so they redraw with rescaled domains instead of
    // skewing geometrically.
    const view = root.append("g")
      .attr("clip-path", `url(#${clipId})`)
      .append("g")
      .attr("class", "uni-view");

    // ── Gridlines (live inside view, redrawn on zoom) ───────────────────
    const gridX = d3.range(xDomain[0], xDomain[1] + 1, 10);
    const gridY = d3.range(yDomain[0], yDomain[1] + 1, 10);
    const gxGroup = view.append("g").attr("class", "gxgroup");
    const gyGroup = view.append("g").attr("class", "gygroup");

    function drawGrid(xs, ys) {
      gxGroup.selectAll("line").data(xs).join("line")
        .attr("x1", d => xScale(d)).attr("x2", d => xScale(d))
        .attr("y1", 0).attr("y2", innerH)
        .attr("stroke", "#e6e0c7").attr("stroke-width", 0.5);
      gyGroup.selectAll("line").data(ys).join("line")
        .attr("x1", 0).attr("x2", innerW)
        .attr("y1", d => yScale(d)).attr("y2", d => yScale(d))
        .attr("stroke", "#e6e0c7").attr("stroke-width", 0.5);
    }
    drawGrid(gridX, gridY);

    // ── Axes (outside view; we rebuild these on zoom from rescaled scales) ──
    const xAxis = d3.axisBottom(xScale).tickValues(gridX).tickFormat(d => `10${supScript(d)}`);
    const yAxis = d3.axisLeft(yScale).tickValues(gridY).tickFormat(d => `10${supScript(d)}`);
    const xAxisG = root.append("g")
      .attr("class", "xaxis")
      .attr("transform", `translate(0,${innerH})`)
      .call(xAxis).call(g => g.selectAll(".domain, .tick line").attr("stroke", "#888"));
    const yAxisG = root.append("g")
      .attr("class", "yaxis")
      .call(yAxis).call(g => g.selectAll(".domain, .tick line").attr("stroke", "#888"));
    root.append("text")
      .attr("x", innerW / 2).attr("y", innerH + 38)
      .attr("text-anchor", "middle").attr("fill", "#444")
      .attr("font-size", 12).attr("font-weight", 600)
      .text("size  →  log₁₀(r / λ_proton)");
    root.append("text")
      .attr("transform", `rotate(-90)`)
      .attr("x", -innerH / 2).attr("y", -42)
      .attr("text-anchor", "middle").attr("fill", "#444")
      .attr("font-size", 12).attr("font-weight", 600)
      .text("mass  →  log₁₀(m / m_proton)");

    // ── Boundary + density diagonal lines (in view group) ──────────────
    // BH boundary: r = 2GM/c² → log(r/λ_p) = log(m/m_p) + log(2G m_p/(c² λ_p))
    // 2G m_p / (c² λ_p) = 2 × 6.674e-11 × 1.673e-27 / (9e16 × 1.32e-15)
    //                  = 2.232e-37 / 1.19e2 = 1.876e-39 (dimensionless)
    // So log(r/λ_p) = log(m/m_p) - 38.73, i.e. y = x + 38.73 in our axes
    // QM boundary: r = ℏ/(mc) → log(r/λ_p) = -log(m/m_p) - 0.8
    const BH_INTERCEPT = 38.73;
    const QM_INTERCEPT = -0.8;

    // For density diagonals: y = 3x + log10(ρ) - 17.24  (see derivation in v0)
    function densityIntercept(rho) { return Math.log10(rho) - 17.24; }

    const lineSpecs = [
      { kind: "bh",      pts: [[xDomain[0], xDomain[0] + BH_INTERCEPT], [xDomain[1], xDomain[1] + BH_INTERCEPT]],
        attrs: { stroke: "#1a1a1a", "stroke-dasharray": "6 3", "stroke-width": 1.6 },
        label: "Black hole boundary", labelDx: -42, labelDy: 250, color: "#1a1a1a" },
      { kind: "qm",      pts: [[xDomain[0], -xDomain[0] + QM_INTERCEPT], [xDomain[1], -xDomain[1] + QM_INTERCEPT]],
        attrs: { stroke: "#1a1a1a", "stroke-dasharray": "6 3", "stroke-width": 1.6 },
        label: "Quantum mechanics boundary", labelDx: 42, labelDy: -150, color: "#1a1a1a" },
      { kind: "nuclear", pts: [[xDomain[0], 3 * xDomain[0] + densityIntercept(2.3e17)], [xDomain[1], 3 * xDomain[1] + densityIntercept(2.3e17)]],
        attrs: { stroke: BAND_COLORS.nuclear, "stroke-dasharray": "4 3", "stroke-width": 1.0 },
        label: "Nuclear density", labelDx: 60, labelDy: 0, color: BAND_COLORS.nuclear },
      { kind: "atomic",  pts: [[xDomain[0], 3 * xDomain[0] + densityIntercept(5e3)], [xDomain[1], 3 * xDomain[1] + densityIntercept(5e3)]],
        attrs: { stroke: BAND_COLORS.atomic, "stroke-dasharray": "4 3", "stroke-width": 1.0 },
        label: "Atomic density", labelDx: 60, labelDy: 0, color: BAND_COLORS.atomic },
      { kind: "dm",      pts: [[xDomain[0], 3 * xDomain[0] + densityIntercept(5e-25)], [xDomain[1], 3 * xDomain[1] + densityIntercept(5e-25)]],
        attrs: { stroke: BAND_COLORS["dark-matter"], "stroke-dasharray": "4 3", "stroke-width": 1.0 },
        label: "Dark-matter density", labelDx: 60, labelDy: 0, color: BAND_COLORS["dark-matter"] },
    ];

    const lineGroup = view.append("g").attr("class", "lines");
    const lineLabelGroup = view.append("g").attr("class", "linelabels");
    lineSpecs.forEach(spec => {
      const ln = lineGroup.append("line")
        .attr("data-kind", spec.kind)
        .attr("x1", xScale(spec.pts[0][0])).attr("y1", yScale(spec.pts[0][1]))
        .attr("x2", xScale(spec.pts[1][0])).attr("y2", yScale(spec.pts[1][1]));
      Object.entries(spec.attrs).forEach(([k, v]) => ln.attr(k, v));
      const mx = (xScale(spec.pts[0][0]) + xScale(spec.pts[1][0])) / 2 + spec.labelDx;
      const my = (yScale(spec.pts[0][1]) + yScale(spec.pts[1][1])) / 2 + spec.labelDy;
      lineLabelGroup.append("text")
        .attr("data-kind", spec.kind)
        .attr("x", mx).attr("y", my)
        .attr("font-size", 10).attr("font-weight", 600)
        .attr("fill", spec.color)
        .text(spec.label);
    });

    // ── Data points + labels ────────────────────────────────────────────
    const ptGroup = view.append("g").attr("class", "points");
    const labelGroup = view.append("g").attr("class", "labels");

    const visibleObjs = data.objects.filter(obj =>
      obj.x_log_r >= xDomain[0] && obj.x_log_r <= xDomain[1] &&
      obj.y_log_m >= yDomain[0] && obj.y_log_m <= yDomain[1]
    );

    visibleObjs.forEach(obj => {
      const px = xScale(obj.x_log_r);
      const py = yScale(obj.y_log_m);
      const g = ptGroup.append("g")
        .attr("transform", `translate(${px},${py})`)
        .attr("data-id", obj.id)
        .style("cursor", "pointer");
      renderShape(g, obj, 4);
      g.append("title").text(obj.name);
      g.on("mouseenter", e => { showTooltip(e, obj); g.select("circle, rect, path").attr("stroke", "#fff").attr("stroke-width", 2); })
       .on("mousemove", e => moveTooltip(e))
       .on("mouseleave", () => { hideTooltip(); g.select("circle, rect, path").attr("stroke", null); });

      labelGroup.append("text")
        .attr("data-id", obj.id)
        .attr("data-prominence", obj.prominence)
        .attr("x", px + 6).attr("y", py + 3)
        .attr("font-size", 9)
        .attr("fill", "#444")
        .style("opacity", visibleAtZoom(obj.prominence, 1) ? 1 : 0)
        .style("pointer-events", "none")
        .text(obj.name);
    });

    // ── Zoom behavior ──────────────────────────────────────────────────
    // Pan + zoom up to 50× into the densest regions. On every event:
    //   1. transform the view group (geometric zoom)
    //   2. recompute axes with rescaled domains so labels read correctly
    //   3. counter-scale shape sizes & label fonts so they don't balloon
    //   4. fade labels in/out by prominence tier
    const ptNodes = ptGroup.selectAll("g[data-id]");
    const labelNodes = labelGroup.selectAll("text[data-id]");

    function applyZoom(transform) {
      view.attr("transform", transform.toString());
      const k = transform.k;

      const xz = transform.rescaleX(xScale);
      const yz = transform.rescaleY(yScale);
      xAxisG.call(xAxis.scale(xz)).call(g => g.selectAll(".domain, .tick line").attr("stroke", "#888"));
      yAxisG.call(yAxis.scale(yz)).call(g => g.selectAll(".domain, .tick line").attr("stroke", "#888"));

      // Counter-scale visual elements so they don't grow with zoom.
      const inv = 1 / k;
      ptNodes.each(function() {
        const node = d3.select(this);
        const t = node.attr("transform");
        // Strip any prior scale() and re-apply translate + counter-scale.
        const m = t.match(/translate\(([^)]+)\)/);
        if (m) node.attr("transform", `translate(${m[1]}) scale(${inv})`);
      });
      labelNodes
        .style("font-size", `${9 * inv}px`)
        .attr("dx", 6 * inv).attr("dy", 3 * inv)
        .style("opacity", function() {
          const p = +d3.select(this).attr("data-prominence");
          return visibleAtZoom(p, k) ? 1 : 0;
        });

      // Counter-scale boundary + density line strokes so they stay crisp.
      lineGroup.selectAll("line").attr("stroke-width", function() {
        const kind = d3.select(this).attr("data-kind");
        return (kind === "bh" || kind === "qm" ? 1.6 : 1.0) * inv;
      });
      lineLabelGroup.selectAll("text")
        .style("font-size", `${10 * inv}px`)
        .style("opacity", k > 4 ? 0 : 1);  // free up the canvas at high zoom
    }

    const zoom = d3.zoom()
      .scaleExtent([1, 50])
      .translateExtent([[0, 0], [innerW, innerH]])
      .extent([[0, 0], [innerW, innerH]])
      .on("zoom", e => applyZoom(e.transform));

    svg.call(zoom);
    applyZoom(d3.zoomIdentity);

    // Reset-zoom button overlay
    root.append("g").attr("class", "reset-zoom")
      .attr("transform", `translate(${innerW - 78}, 8)`)
      .style("cursor", "pointer")
      .on("click", () => svg.transition().duration(350).call(zoom.transform, d3.zoomIdentity))
      .call(g => {
        g.append("rect")
          .attr("width", 70).attr("height", 22).attr("rx", 4)
          .attr("fill", "#fdfcf6").attr("stroke", "#bbb");
        g.append("text").attr("x", 35).attr("y", 15)
          .attr("text-anchor", "middle").attr("font-size", 10)
          .attr("fill", "#555").text("reset zoom");
      });

    // ── Legend ──────────────────────────────────────────────────────────
    const legendEl = d3.select("#legend-mass-size");
    Object.entries(BAND_LABELS).forEach(([band, label]) => {
      legendEl.append("span").attr("class", "uni-chip").attr("data-band", band)
        .html(`<span class="uni-chip-dot" style="background:${BAND_COLORS[band]}"></span>${label}`);
    });
  }

  // ─────────────────────────────────────────────────────────────────────
  // CHART 2 — Density × Time
  //
  // X-axis is log(time since Big Bang in seconds). The Big Bang sits just
  // off the left edge (Planck time = 5.39e-44 s ≈ 10⁻⁴³·³ s), and "now"
  // sits at log10(4.355e17) ≈ 17.64 on the right. This is the only frame
  // that lets the early-universe expansion (Planck era → inflation →
  // nucleosynthesis → recombination) read as anything other than a single
  // pixel pile-up at the Big Bang.
  //
  // Y-axis is log10(density kg/m³), bounded to the physically meaningful
  // range [-30, +100]. Soft horizontal bands mark cosmic / atomic /
  // nuclear / trans-Planckian regimes, in the same colors as Chart 1.
  // ─────────────────────────────────────────────────────────────────────
  function buildDensityTimeChart() {
    const containerEl = document.getElementById("chart-density-time");
    if (!containerEl) return;
    const W = containerEl.clientWidth;
    const H = containerEl.clientHeight;
    const margin = { top: 28, right: 24, bottom: 56, left: 64 };
    const innerW = W - margin.left - margin.right;
    const innerH = H - margin.top - margin.bottom;

    const svg = d3.select(containerEl).append("svg")
      .attr("viewBox", `0 0 ${W} ${H}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .style("width", "100%").style("height", "100%");

    // x = log10(seconds since Big Bang)
    const xLogDomain = [-44, 18.5]; // Planck time → ~3× universe age (room for "future")
    const yLogDomain = [-30, 100];

    const xScale = d3.scaleLinear().domain(xLogDomain).range([0, innerW]);
    const yScale = d3.scaleLinear().domain(yLogDomain).range([innerH, 0]);

    const root = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    root.append("rect")
      .attr("width", innerW).attr("height", innerH)
      .attr("fill", "#fdfcf6").attr("stroke", "#cdc8b6");

    // ── Density bands (mirror Chart 1 color scheme) ─────────────────────
    const bands = [
      { y: [-29, -22], color: BAND_COLORS["dark-matter"], label: "Dark-matter / cosmic", op: 0.07 },
      { y: [-22,  3],  color: null,                       label: "Diffuse",              op: 0 },
      { y: [ 3,   6],  color: BAND_COLORS.atomic,         label: "Atomic / solid",       op: 0.07 },
      { y: [ 6,  15],  color: null,                       label: "Degenerate",           op: 0 },
      { y: [15,  20],  color: BAND_COLORS.nuclear,        label: "Nuclear",              op: 0.10 },
      { y: [20,  99],  color: BAND_COLORS.planck,         label: "Trans-Planckian",      op: 0.06 },
    ];
    bands.forEach(b => {
      if (b.op === 0) return;
      root.append("rect")
        .attr("x", 0).attr("width", innerW)
        .attr("y", yScale(b.y[1])).attr("height", yScale(b.y[0]) - yScale(b.y[1]))
        .attr("fill", b.color).attr("opacity", b.op);
    });

    // ── Gridlines ───────────────────────────────────────────────────────
    const gridX = d3.range(Math.ceil(xLogDomain[0] / 4) * 4, xLogDomain[1] + 1, 4);
    const gridY = d3.range(yLogDomain[0], yLogDomain[1] + 1, 10);
    root.append("g").selectAll("line.gx").data(gridX).join("line")
      .attr("x1", d => xScale(d)).attr("x2", d => xScale(d))
      .attr("y1", 0).attr("y2", innerH)
      .attr("stroke", "#e6e0c7").attr("stroke-width", 0.5);
    root.append("g").selectAll("line.gy").data(gridY).join("line")
      .attr("x1", 0).attr("x2", innerW)
      .attr("y1", d => yScale(d)).attr("y2", d => yScale(d))
      .attr("stroke", "#e6e0c7").attr("stroke-width", 0.5);

    // ── Era markers (vertical lines at well-known cosmic times) ─────────
    const NOW_LOG = Math.log10(UNIVERSE_AGE_S);
    const eras = [
      { logT: -43.27, label: "Planck",       short: "tₚ" },
      { logT: -32,    label: "Inflation end" },
      { logT: -5,     label: "QCD" },
      { logT: 2.26,   label: "Nucleosynth." },
      { logT: 13.08,  label: "Recombination" },
      { logT: 15.80,  label: "First stars" },
      { logT: Math.log10(UNIVERSE_AGE_S - 4.6e9 * SECONDS_PER_YEAR), label: "Solar system" },
      { logT: NOW_LOG, label: "Now", emphasis: true },
    ];
    eras.forEach((e, i) => {
      const x = xScale(e.logT);
      if (x < 0 || x > innerW) return;
      root.append("line")
        .attr("x1", x).attr("x2", x).attr("y1", 0).attr("y2", innerH)
        .attr("stroke", e.emphasis ? "#888" : "#cfc8b3")
        .attr("stroke-dasharray", e.emphasis ? null : "3 3")
        .attr("stroke-width", e.emphasis ? 1.0 : 0.6);
      root.append("text").attr("x", x).attr("y", -8)
        .attr("text-anchor", "middle").attr("font-size", 9)
        .attr("fill", e.emphasis ? "#444" : "#888")
        .text(e.label);
    });

    // ── Axes ────────────────────────────────────────────────────────────
    const xAxis = d3.axisBottom(xScale)
      .tickValues(gridX)
      .tickFormat(d => formatLogSeconds(d));
    const yAxis = d3.axisLeft(yScale)
      .tickValues(gridY)
      .tickFormat(d => `10${supScript(d)}`);
    root.append("g").attr("transform", `translate(0,${innerH})`).call(xAxis)
      .call(g => g.selectAll("text").attr("font-size", 9))
      .call(g => g.selectAll(".domain, .tick line").attr("stroke", "#888"));
    root.append("g").call(yAxis)
      .call(g => g.selectAll("text").attr("font-size", 10))
      .call(g => g.selectAll(".domain, .tick line").attr("stroke", "#888"));
    root.append("text")
      .attr("x", innerW / 2).attr("y", innerH + 40)
      .attr("text-anchor", "middle").attr("fill", "#444")
      .attr("font-size", 12).attr("font-weight", 600)
      .text("time since Big Bang  →  log₁₀(t / s)");
    root.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -innerH / 2).attr("y", -46)
      .attr("text-anchor", "middle").attr("fill", "#444")
      .attr("font-size", 12).attr("font-weight", 600)
      .text("density  →  log₁₀(ρ / kg·m⁻³)");

    // ── Universe trace ──────────────────────────────────────────────────
    const universeObj = data.objects.find(o => o.id === "observable-universe");
    if (universeObj && universeObj.evolution) {
      const evo = universeObj.evolution
        .map(d => ({
          ...d,
          x_log_t: Math.log10(Math.max(d.time_after_bb_s, PLANCK_TIME_S)),
          y_log_d: Math.log10(d.density_kg_m3),
        }))
        .sort((a, b) => a.x_log_t - b.x_log_t);

      // Background "shadow" stroke for legibility
      const lineGen = d3.line()
        .x(d => xScale(d.x_log_t))
        .y(d => yScale(d.y_log_d))
        .curve(d3.curveMonotoneX);

      root.append("path")
        .datum(evo)
        .attr("fill", "none")
        .attr("stroke", "#fffceb")
        .attr("stroke-width", 5)
        .attr("stroke-linecap", "round")
        .attr("d", lineGen);
      root.append("path")
        .datum(evo)
        .attr("fill", "none")
        .attr("stroke", "#3a3a3a")
        .attr("stroke-width", 2)
        .attr("stroke-linecap", "round")
        .attr("d", lineGen);

      // Per-segment colored overlays — paint each segment in the band
      // color of its starting waypoint, so the trace bleeds from Planck
      // through nuclear → atomic → cosmic.
      for (let i = 0; i < evo.length - 1; i++) {
        const a = evo[i], b = evo[i + 1];
        const segColor = bandColorForDensity(a.density_kg_m3);
        root.append("path")
          .datum([a, b])
          .attr("fill", "none")
          .attr("stroke", segColor)
          .attr("stroke-width", 2.5)
          .attr("stroke-linecap", "round")
          .attr("opacity", 0.85)
          .attr("d", lineGen);
      }

      // Waypoint dots
      root.selectAll("circle.uni-evo").data(evo).join("circle")
        .attr("class", "uni-evo")
        .attr("cx", d => xScale(d.x_log_t))
        .attr("cy", d => yScale(d.y_log_d))
        .attr("r", 4)
        .attr("fill", d => bandColorForDensity(d.density_kg_m3))
        .attr("stroke", "#fffceb")
        .attr("stroke-width", 1.2)
        .style("cursor", "pointer")
        .on("mouseenter", (e, d) => {
          tooltip.html(
            `<strong>Universe — ${d.label}</strong>` +
            `<div class="meta">density ≈ ${formatScientific(d.density_kg_m3, "kg/m³")}</div>` +
            `<div class="meta">t = ${formatScientific(d.time_after_bb_s, "s")} after Big Bang</div>`
          )
            .style("left", (e.clientX + 14) + "px").style("top", (e.clientY + 14) + "px")
            .style("opacity", 1);
        })
        .on("mousemove", e => moveTooltip(e))
        .on("mouseleave", hideTooltip);
    }

    // ── All other objects ──────────────────────────────────────────────
    data.objects.forEach(obj => {
      if (obj.id === "observable-universe") return;
      if (!obj.formation || obj.formation.time_after_bb_s == null) return;
      const t = obj.formation.time_after_bb_s;
      const d = obj.density_kg_m3;
      if (d <= 0 || t <= 0) return;
      const x_log = Math.log10(Math.max(t, PLANCK_TIME_S));
      const y_log = Math.log10(d);
      if (x_log < xLogDomain[0] || x_log > xLogDomain[1]) return;
      if (y_log < yLogDomain[0] || y_log > yLogDomain[1]) return;
      const px = xScale(x_log);
      const py = yScale(y_log);
      const g = root.append("g")
        .attr("transform", `translate(${px},${py})`)
        .attr("data-id", obj.id)
        .style("cursor", "pointer");
      renderShape(g, obj, 4);
      g.on("mouseenter", e => { showTooltip(e, obj); g.select("circle, rect, path").attr("stroke", "#fff").attr("stroke-width", 2); })
       .on("mousemove", moveTooltip)
       .on("mouseleave", () => { hideTooltip(); g.select("circle, rect, path").attr("stroke", null); });

      // Inline label
      root.append("text")
        .attr("x", px + 6).attr("y", py + 3)
        .attr("font-size", 9).attr("fill", "#444")
        .text(obj.name);
    });

    // ── Legend ──────────────────────────────────────────────────────────
    const legendEl = d3.select("#legend-density-time");
    legendEl.html("");
    bands.forEach(b => {
      if (b.op === 0) return;
      legendEl.append("span").attr("class", "uni-chip")
        .html(`<span class="uni-chip-dot" style="background:${b.color}"></span>${b.label}`);
    });
    legendEl.append("span").attr("class", "uni-chip")
      .html(`<span class="uni-chip-dot" style="background:#3a3a3a"></span>Universe trace`);
  }

  // Format a log10(seconds) tick into an intuitive label like "1 s",
  // "1 yr ago" or "10⁻³² s". Edge cases: very small → exponent only;
  // around present → human units.
  function formatLogSeconds(logT) {
    const t = Math.pow(10, logT);
    const NOW_LOG = Math.log10(UNIVERSE_AGE_S);
    if (Math.abs(logT - NOW_LOG) < 0.4) return "now";
    if (logT < -10)   return `10${supScript(Math.round(logT))} s`;
    if (logT < 0)     return `10${supScript(Math.round(logT))} s`;
    if (logT < 2)     return `${Math.round(t)} s`;
    if (logT < 4.5)   return `${Math.round(t / 60)} min`;
    if (logT < 7.5)   return `${Math.round(t / SECONDS_PER_YEAR / 1).toLocaleString()} yr`;
    if (logT < 10.5)  return `${(t / SECONDS_PER_YEAR / 1e6).toFixed(0)} Myr`;
    if (logT < 18)    return `${(t / SECONDS_PER_YEAR / 1e9).toFixed(1)} Gyr`;
    return `10${supScript(Math.round(logT))} s`;
  }

  function bandColorForDensity(rho) {
    if (rho >= 1e20) return BAND_COLORS.planck;
    if (rho >= 1e15) return BAND_COLORS.nuclear;
    if (rho >= 5e2)  return BAND_COLORS.atomic;
    if (rho >= 1e-22) return BAND_COLORS["dark-matter"];
    return BAND_COLORS.radiation;
  }

  function drawLine(root, xScale, yScale, p1, p2, attrs, labelText, labelDx, labelDy, labelColor) {
    const line = root.append("line")
      .attr("x1", xScale(p1[0])).attr("y1", yScale(p1[1]))
      .attr("x2", xScale(p2[0])).attr("y2", yScale(p2[1]));
    Object.entries(attrs).forEach(([k, v]) => line.attr(k, v));
    if (labelText) {
      // Place label near midpoint with offset
      const mx = (xScale(p1[0]) + xScale(p2[0])) / 2 + labelDx;
      const my = (yScale(p1[1]) + yScale(p2[1])) / 2 + labelDy;
      root.append("text")
        .attr("x", mx).attr("y", my)
        .attr("font-size", 10).attr("font-weight", 600)
        .attr("fill", labelColor || "#444")
        .text(labelText);
    }
  }

  function supScript(n) {
    const map = { "0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹","-":"⁻" };
    return String(n).split("").map(c => map[c] || c).join("");
  }

  // ── Boot ─────────────────────────────────────────────────────────────
  // main.js sits at end-of-body, so DOMContentLoaded usually fires BEFORE
  // this code runs. Listening for it is too late — invoke directly if the
  // document is already past loading.
  function boot() {
    try {
      buildMassSizeChart();
      buildDensityTimeChart();
    } catch (e) {
      console.error("[universe] chart init failed:", e);
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
