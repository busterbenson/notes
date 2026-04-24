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

  // Prominence tier (1-4) controls whether a marker AND its label
  // render at a given zoom level. Tuned so the default view shows
  // ~10 anchor objects without overlap, and progressively richer
  // populations appear as the user zooms in:
  //   k=1  → tier 1 (~10 anchors)
  //   k≥2  → tier 2 adds (planets, major stars, galaxies, compacts, cells)
  //   k≥4  → tier 3 adds (more animals, atoms, asteroids, viruses, smaller structures)
  //   k≥8  → tier 4 (every exotic particle, every atom, every minor moon)
  function labelProminence(o) {
    if (o.prominence != null) return +o.prominence; // explicit override from yaml
    const tier1 = new Set([
      "observable-universe", "milky-way", "sgr-a",
      "sun", "earth",
      "human", "eukaryotic-cell",
      "proton", "electron",
    ]);
    const tier2 = new Set([
      // Galaxies + clusters — well-separated on the chart, can show at k≥2
      "andromeda", "laniakea", "virgo-cluster",
      "m33-triangulum", "lmc",
      // Solar system / stars — show one anchor each
      "jupiter", "moon", "sirius-a",
      // One iconic compact object per family
      "m87-smbh", "crab-pulsar", "stellar-bh",
      // Familiar large-scale things
      "blue-whale", "elephant",
      "sars-cov-2",
      "uranium-atom",
      "neutrino",
      "mount-everest", "great-barrier-reef", "titanic", "cumulus-cloud",
    ]);
    if (tier1.has(o.id)) return 1;
    if (tier2.has(o.id)) return 2;
    if (o.category === "planet" || o.category === "star") return 3;
    if (o.category === "galaxy" || o.category === "cluster") return 3;
    if (o.category === "compact-object" || o.category === "structure") return 3;
    if (o.category === "organism" || o.category === "cell") return 3;
    if (o.category === "virus" || o.category === "macromolecule") return 3;
    return 4;
  }

  function visibleAtZoom(prominence, k) {
    if (k >= 8) return true;
    if (k >= 4) return prominence <= 3;
    if (k >= 2) return prominence <= 2;
    return prominence <= 1;
  }

  // ── Tour mode ────────────────────────────────────────────────────────
  // A guided 12-stop walk from the largest known structure down to the
  // electron — the same scale ladder the page is built around. Each
  // stop highlights the object on both charts via crossChartHover()
  // and surfaces a one-line story; auto-advances every 4 seconds.
  const TOUR_STOPS = [
    { id: "observable-universe",
      story: "Everything we can see — 93 billion light-years across in proper distance, 13.8 Gyr old. The whole chart is contained in this one dot." },
    { id: "laniakea",
      story: "Our home supercluster. 100,000 galaxies including the Milky Way, gravitationally drifting toward the Great Attractor." },
    { id: "milky-way",
      story: "Our barred-spiral galaxy. ~200 billion stars across a 100,000-light-year disk." },
    { id: "sgr-a",
      story: "The supermassive black hole at the Milky Way's center. 4.3 million solar masses crammed inside a Schwarzschild radius the size of Mercury's orbit." },
    { id: "sun",
      story: "G2V main-sequence star. 4.6 Gyr old, ~5 Gyr remaining before red-giant phase." },
    { id: "earth",
      story: "Our planet. ~5,500 kg/m³ — densest in the solar system because of the iron core." },
    { id: "blue-whale",
      story: "Largest animal that has ever lived. Mass ~150 tonnes, density just above water." },
    { id: "human",
      story: "Median adult — about 70 kg, 1.7 m, density slightly above water. Big enough to think, small enough to fit inside the atomic-density slope." },
    { id: "eukaryotic-cell",
      story: "A typical eukaryotic cell. The transition from inanimate matter to organism happens 6 orders of magnitude below us." },
    { id: "sars-cov-2",
      story: "A SARS-CoV-2 virion — about 100 nm across. Self-replicating organic chemistry just barely qualifies as 'alive.'" },
    { id: "proton",
      story: "A proton. The reference particle for both axes — every label is normalized to its mass and Compton wavelength." },
    { id: "electron",
      story: "An electron. Sits on the quantum-mechanics boundary line: any smaller and the uncertainty principle blurs out its position." },
  ];

  let tourTimer = null;
  let tourIdx = 0;
  let tourActive = false;

  function startTour() {
    tourActive = true;
    tourIdx = 0;
    showTourStep();
    document.getElementById("uni-tour-controls").style.display = "flex";
    document.getElementById("uni-tour-button").style.display = "none";
  }
  function stopTour() {
    tourActive = false;
    if (tourTimer) clearTimeout(tourTimer);
    crossChartClear();
    hideTourCard();
    document.getElementById("uni-tour-controls").style.display = "none";
    document.getElementById("uni-tour-button").style.display = "inline-flex";
  }
  function tourNext() {
    if (!tourActive) return;
    tourIdx = (tourIdx + 1) % TOUR_STOPS.length;
    showTourStep();
  }
  function tourPrev() {
    if (!tourActive) return;
    tourIdx = (tourIdx - 1 + TOUR_STOPS.length) % TOUR_STOPS.length;
    showTourStep();
  }
  function showTourStep() {
    if (tourTimer) clearTimeout(tourTimer);
    const stop = TOUR_STOPS[tourIdx];
    const obj = data.objects.find(o => o.id === stop.id);
    if (!obj) { tourNext(); return; }
    crossChartHover(stop.id);
    showTourCard(obj, stop.story, tourIdx + 1, TOUR_STOPS.length);
    tourTimer = setTimeout(tourNext, 4500);
  }
  function showTourCard(obj, story, n, total) {
    const card = document.getElementById("uni-tour-card");
    card.style.display = "block";
    card.innerHTML =
      `<div class="uni-tour-counter">${n} / ${total}</div>` +
      `<div class="uni-tour-name">${obj.name}</div>` +
      `<div class="uni-tour-story">${story}</div>`;
  }
  function hideTourCard() {
    const card = document.getElementById("uni-tour-card");
    if (card) card.style.display = "none";
  }

  // ── Cross-chart linking ──────────────────────────────────────────────
  // When an object is hovered on either chart, fade everyone else on
  // BOTH charts and spotlight the matching id. Lets the eye trace
  // an object from its mass-radius position to its time-density
  // counterpart without losing context.
  const CROSS_LINK_SELECTOR = "g[data-id]";
  const CROSS_LINK_LABEL_SELECTOR = "text[data-id]";
  function crossChartHover(id) {
    document.querySelectorAll(CROSS_LINK_SELECTOR).forEach(node => {
      if (node.getAttribute("data-id") === id) {
        node.classList.add("uni-spot");
        node.classList.remove("uni-dimmed");
      } else {
        node.classList.add("uni-dimmed");
        node.classList.remove("uni-spot");
      }
    });
    // Pop the matching label OUT regardless of its prominence tier so
    // even hidden cluster members become readable when hovered. The
    // CSS class force-shows it, raises it above siblings, and gives
    // it a white pill background so it cuts through any overlap.
    document.querySelectorAll(CROSS_LINK_LABEL_SELECTOR).forEach(node => {
      if (node.getAttribute("data-id") === id) {
        node.classList.add("uni-label-spot");
        // Move to end of parent so it paints on top.
        if (node.parentNode) node.parentNode.appendChild(node);
      } else {
        node.classList.add("uni-label-dimmed");
      }
    });
  }
  function crossChartClear() {
    document.querySelectorAll(CROSS_LINK_SELECTOR).forEach(node => {
      node.classList.remove("uni-dimmed");
      node.classList.remove("uni-spot");
    });
    document.querySelectorAll(CROSS_LINK_LABEL_SELECTOR).forEach(node => {
      node.classList.remove("uni-label-spot");
      node.classList.remove("uni-label-dimmed");
    });
  }

  // ── Tooltip ──────────────────────────────────────────────────────────
  const tooltip = d3.select("#uni-tooltip");

  // Anchor the tooltip on the MARKER's screen position, not the mouse
  // cursor. Otherwise zoomed views move the marker but the tooltip
  // tracks the cursor and they drift apart visually. The mousemove
  // handler is a no-op so the tooltip stays put while hovering.
  function showTooltip(event, obj) {
    const lines = [
      `<strong>${obj.name}</strong>`,
      `<div class="meta">${formatScientific(obj.mass_kg, "kg")} · ${formatScientific(obj.radius_m, "m")} · ${formatScientific(obj.density_kg_m3, "kg/m³")}</div>`,
      obj.blurb ? `<div style="margin-top:0.35rem;">${obj.blurb}</div>` : "",
    ].join("");
    tooltip.html(lines);
    placeTooltipAtMarker(event.currentTarget);
    tooltip.style("opacity", 1);
  }
  function placeTooltipAtMarker(markerNode) {
    if (!markerNode || !markerNode.getBoundingClientRect) return;
    const r = markerNode.getBoundingClientRect();
    const ttEl = tooltip.node();
    if (!ttEl) return;
    const ttW = ttEl.offsetWidth || 280;
    const ttH = ttEl.offsetHeight || 60;
    // getBoundingClientRect is viewport-relative; the tooltip uses
    // position:absolute so its left/top are document-relative — add
    // scroll offsets so the card lands next to the marker even when
    // the page has been scrolled.
    const sx = window.pageXOffset || document.documentElement.scrollLeft;
    const sy = window.pageYOffset || document.documentElement.scrollTop;
    // Default: tooltip to the right of the marker, vertically centered.
    let left = r.right + 10 + sx;
    let top  = r.top + r.height / 2 - ttH / 2 + sy;
    // If we'd run off the right edge of the viewport, swap to left side.
    if (r.right + 10 + ttW > window.innerWidth - 8) {
      left = r.left - ttW - 10 + sx;
    }
    // Clamp viewport bounds (still in viewport coords for the clamp,
    // then re-apply scroll to convert back to document coords).
    let topVp = top - sy;
    topVp = Math.max(8, Math.min(topVp, window.innerHeight - ttH - 8));
    top = topVp + sy;
    tooltip.style("left", left + "px").style("top", top + "px");
  }
  function moveTooltip(_event) {
    // No-op — tooltip stays anchored to the marker for the duration
    // of the hover. Re-anchoring on mousemove caused jitter when the
    // cursor wandered between the marker and the tooltip itself.
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

    // Each spec specifies the line slope/intercept (data coords) plus
    // an `anchorX` — the data x where we place the label. The label
    // sits ON the line at that x, rotated to match the screen-space
    // slope, and offset perpendicular by ~10px so it floats just
    // above/below the dashed stroke.
    //
    // anchorX picked so the labels DON'T cross adjacent lines. Density
    // diagonals (slope 3) are stacked with intercepts ~17 apart in y;
    // each label sits at a different x to avoid stacking up.
    const lineSpecs = [
      // Hard boundaries — black, near opposite corners of the chart.
      { kind: "bh",      slope: 1,  intercept: BH_INTERCEPT,
        anchorX: 8,  perpOffset: -10,
        attrs: { stroke: "#1a1a1a", "stroke-dasharray": "6 3", "stroke-width": 1.6 },
        label: "Black hole boundary", color: "#1a1a1a" },
      { kind: "qm",      slope: -1, intercept: QM_INTERCEPT,
        anchorX: -16, perpOffset: -10,
        attrs: { stroke: "#1a1a1a", "stroke-dasharray": "6 3", "stroke-width": 1.6 },
        label: "Quantum mechanics boundary", color: "#1a1a1a" },
      // Density diagonals — stacked, anchored at progressively higher
      // x so the labels spread along a NW-SE direction across the
      // visible area.
      { kind: "nuclear", slope: 3,  intercept: densityIntercept(2.3e17),
        anchorX: 12, perpOffset: -10,
        attrs: { stroke: BAND_COLORS.nuclear, "stroke-dasharray": "4 3", "stroke-width": 1.0 },
        label: "Nuclear density", color: BAND_COLORS.nuclear },
      { kind: "atomic",  slope: 3,  intercept: densityIntercept(5e3),
        anchorX: 17, perpOffset: -10,
        attrs: { stroke: BAND_COLORS.atomic, "stroke-dasharray": "4 3", "stroke-width": 1.0 },
        label: "Atomic density", color: BAND_COLORS.atomic },
      { kind: "dm",      slope: 3,  intercept: densityIntercept(5e-25),
        anchorX: 28, perpOffset: -10,
        attrs: { stroke: BAND_COLORS["dark-matter"], "stroke-dasharray": "4 3", "stroke-width": 1.0 },
        label: "Dark-matter density", color: BAND_COLORS["dark-matter"] },
      // ρ_Λ ≈ 5.96e-27 kg/m³ — vacuum energy density from the
      // cosmological constant (Planck 2018). Outer bound on how
      // empty space can be; cosmic voids and "empty" space asymptote
      // here. Drawn black as a hard boundary like BH/QM.
      { kind: "vacuum",  slope: 3,  intercept: densityIntercept(5.96e-27),
        anchorX: 33, perpOffset: -10,
        attrs: { stroke: "#1a1a1a", "stroke-dasharray": "2 4", "stroke-width": 1.6 },
        label: "Vacuum (Λ)", color: "#1a1a1a" },
    ];

    const lineGroup = view.append("g").attr("class", "lines");
    const lineLabelGroup = view.append("g").attr("class", "linelabels");
    lineSpecs.forEach(spec => {
      const x1 = xDomain[0], x2 = xDomain[1];
      const y1 = spec.slope * x1 + spec.intercept;
      const y2 = spec.slope * x2 + spec.intercept;
      const sx1 = xScale(x1), sy1 = yScale(y1), sx2 = xScale(x2), sy2 = yScale(y2);

      const ln = lineGroup.append("line")
        .attr("data-kind", spec.kind)
        .attr("x1", sx1).attr("y1", sy1).attr("x2", sx2).attr("y2", sy2);
      Object.entries(spec.attrs).forEach(([k, v]) => ln.attr(k, v));

      // Place label on the line at anchorX, then offset perpendicular
      // to the line direction so it doesn't sit directly on the stroke.
      const yAnchor = spec.slope * spec.anchorX + spec.intercept;
      const px = xScale(spec.anchorX);
      const py = yScale(yAnchor);
      const dx = sx2 - sx1, dy = sy2 - sy1;
      const len = Math.hypot(dx, dy) || 1;
      // Perpendicular unit vector pointing "up" in screen space (negative y).
      let perpX = -dy / len, perpY = dx / len;
      if (perpY > 0) { perpX = -perpX; perpY = -perpY; }
      const lx = px + perpX * spec.perpOffset;
      const ly = py + perpY * spec.perpOffset;
      const angleDeg = Math.atan2(dy, dx) * 180 / Math.PI;

      lineLabelGroup.append("text")
        .attr("data-kind", spec.kind)
        .attr("x", lx).attr("y", ly)
        .attr("text-anchor", "middle")
        .attr("font-size", 10).attr("font-weight", 600)
        .attr("fill", spec.color)
        .attr("transform", `rotate(${angleDeg} ${lx} ${ly})`)
        .text(spec.label);
    });

    // ── Data points + labels ────────────────────────────────────────────
    // Markers go inside the view group (zoom transforms them).
    // Labels go in a SEPARATE group attached to root (outside zoom),
    // because text inside a scaled group sees its dx/dy multiplied by
    // the zoom factor — so labels drift away from their markers as you
    // zoom in. Storing data-px / data-py on each label lets us
    // recompute screen position on every zoom event using the
    // rescaled axes.
    const ptGroup = view.append("g").attr("class", "points");
    const labelGroup = root.append("g").attr("class", "labels")
      .attr("clip-path", `url(#${clipId})`);

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
        .attr("data-band", obj.color_band)
        .attr("data-prominence", obj.prominence)
        .style("cursor", "pointer")
        .style("opacity", visibleAtZoom(obj.prominence, 1) ? 1 : 0);
      renderShape(g, obj, 4);
      g.append("title").text(obj.name);
      g.on("mouseenter", e => { showTooltip(e, obj); crossChartHover(obj.id); })
       .on("mousemove", e => moveTooltip(e))
       .on("mouseleave", () => { hideTooltip(); crossChartClear(); });

      labelGroup.append("text")
        .attr("data-id", obj.id)
        .attr("data-band", obj.color_band)
        .attr("data-prominence", obj.prominence)
        .attr("data-x-log", obj.x_log_r)
        .attr("data-y-log", obj.y_log_m)
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

      // Counter-scale markers so the shapes don't balloon with zoom.
      // Markers also fade by prominence — at base zoom only headline
      // objects show, more reveal as you zoom in.
      const inv = 1 / k;
      ptNodes.each(function() {
        const node = d3.select(this);
        const t = node.attr("transform");
        const m = t.match(/translate\(([^)]+)\)/);
        if (m) node.attr("transform", `translate(${m[1]}) scale(${inv})`);
        const p = +node.attr("data-prominence");
        if (!isNaN(p)) node.style("opacity", visibleAtZoom(p, k) ? 1 : 0);
      });

      // Labels live OUTSIDE the zoomed view group, so we re-anchor them
      // to the marker's screen position using the rescaled axes. This
      // keeps each label exactly 6/3 px from its marker at any zoom
      // level instead of drifting away as the zoom factor multiplies
      // dx/dy inside a scaled coordinate space.
      labelNodes.each(function() {
        const node = d3.select(this);
        const xLog = +node.attr("data-x-log");
        const yLog = +node.attr("data-y-log");
        node.attr("x", xz(xLog) + 6).attr("y", yz(yLog) + 3);
        const p = +node.attr("data-prominence");
        node.style("opacity", visibleAtZoom(p, k) ? 1 : 0);
      });

      // Counter-scale boundary + density line strokes so they stay crisp.
      // BH, QM, and Vacuum are hard boundaries → thicker stroke.
      lineGroup.selectAll("line").attr("stroke-width", function() {
        const kind = d3.select(this).attr("data-kind");
        const isBoundary = kind === "bh" || kind === "qm" || kind === "vacuum";
        return (isBoundary ? 1.6 : 1.0) * inv;
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

    // ── Legend (clickable to toggle bands + boundaries) ─────────────────
    const legendEl = d3.select("#legend-mass-size");
    const bandToLineKind = { nuclear: "nuclear", atomic: "atomic", "dark-matter": "dm" };
    Object.entries(BAND_LABELS).forEach(([band, label]) => {
      const chip = legendEl.append("span")
        .attr("class", "uni-chip").attr("data-band", band).attr("data-on", "true")
        .html(`<span class="uni-chip-dot" style="background:${BAND_COLORS[band]}"></span>${label}`);
      chip.on("click", function() {
        const on = this.getAttribute("data-on") !== "false";
        const next = on ? "false" : "true";
        this.setAttribute("data-on", next);
        toggleBandVisibility(band, !on);
      });
    });
    // Add boundary toggles as bonus chips
    [{ kind: "bh", label: "Black hole boundary" }, { kind: "qm", label: "Quantum mechanics boundary" }].forEach(({ kind, label }) => {
      const chip = legendEl.append("span")
        .attr("class", "uni-chip").attr("data-line-kind", kind).attr("data-on", "true")
        .html(`<span class="uni-chip-dot" style="background:#1a1a1a"></span>${label}`);
      chip.on("click", function() {
        const on = this.getAttribute("data-on") !== "false";
        const next = on ? "false" : "true";
        this.setAttribute("data-on", next);
        toggleLineKindVisibility(kind, !on);
      });
    });

    function toggleBandVisibility(band, visible) {
      const op = visible ? "" : "none";
      view.selectAll(`g[data-band="${band}"]`).style("display", op);
      labelGroup.selectAll(`text[data-band="${band}"]`).style("display", op);
      const lineKind = bandToLineKind[band];
      if (lineKind) toggleLineKindVisibility(lineKind, visible);
    }
    function toggleLineKindVisibility(kind, visible) {
      const op = visible ? "" : "none";
      lineGroup.select(`line[data-kind="${kind}"]`).style("display", op);
      lineLabelGroup.select(`text[data-kind="${kind}"]`).style("display", op);
    }
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

    // X-AXIS REWRITE 2026-04-23 — symmetric log centered on NOW.
    //
    // The eye lives in the present. Everything important happens in the
    // last few decades; everything ancient compresses into the leftmost
    // sliver. d3.scaleSymlog with constant=1 gives a linear vicinity of
    // ±1 second around now and a logarithmic stretch in both directions
    // outside that. The Big Bang (-4.355e17 s) sits at the far left;
    // the heat death of the universe (way out in the future) sits at
    // the far right. "1 day ago" and "1 day from now" are equidistant
    // from center. Most pixels are spent on the most recent and most
    // imminent moments.
    const PAST_LIMIT_S   = -UNIVERSE_AGE_S;        // Big Bang, ~ -4.355e17 s
    const FUTURE_LIMIT_S = UNIVERSE_AGE_S * 2.0;   // ~ +8.7e17 s, far enough for stellar futures
    const yLogDomain = [-30, 100];

    const xScale = d3.scaleSymlog()
      .domain([PAST_LIMIT_S, FUTURE_LIMIT_S])
      .range([0, innerW])
      .constant(1);  // linear within ±1s around now, log outside
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

    // ── Tick values ──────────────────────────────────────────────────────
    // Hand-picked symmetric anchors so labels read as familiar units
    // ("1 yr ago", "1 yr from now") rather than scientific notation.
    const yearS = SECONDS_PER_YEAR;
    const anchorTicks = [
      -1e10 * yearS, -1e9 * yearS, -1e8 * yearS, -1e7 * yearS,
      -1e6 * yearS, -1e5 * yearS, -1e4 * yearS, -1e3 * yearS,
      -100 * yearS, -10 * yearS, -1 * yearS,
      -86400 * 30, -86400, -3600, -60, -1,
      0,
      1, 60, 3600, 86400, 86400 * 30,
      1 * yearS, 10 * yearS, 100 * yearS, 1e3 * yearS,
      1e4 * yearS, 1e5 * yearS, 1e6 * yearS, 1e7 * yearS,
      1e8 * yearS, 1e9 * yearS,
    ];
    const visibleTicks = anchorTicks.filter(t => t >= PAST_LIMIT_S && t <= FUTURE_LIMIT_S);

    // Gridlines at the same anchor positions.
    const gridY = d3.range(yLogDomain[0], yLogDomain[1] + 1, 10);
    root.append("g").selectAll("line.gx").data(visibleTicks).join("line")
      .attr("x1", d => xScale(d)).attr("x2", d => xScale(d))
      .attr("y1", 0).attr("y2", innerH)
      .attr("stroke", d => d === 0 ? "#888" : "#e6e0c7")
      .attr("stroke-width", d => d === 0 ? 1 : 0.5);
    root.append("g").selectAll("line.gy").data(gridY).join("line")
      .attr("x1", 0).attr("x2", innerW)
      .attr("y1", d => yScale(d)).attr("y2", d => yScale(d))
      .attr("stroke", "#e6e0c7").attr("stroke-width", 0.5);

    // ── Era markers (well-known moments, plotted at their offset from NOW) ──
    const eras = [
      { tFromNow: -UNIVERSE_AGE_S,                          label: "Big Bang" },
      { tFromNow: -(1.36e10 * yearS),                       label: "First stars" },
      { tFromNow: -(4.6e9 * yearS),                         label: "Solar system" },
      { tFromNow: -(3.5e9 * yearS),                         label: "Life begins" },
      { tFromNow: -(6.6e7 * yearS),                         label: "Dinosaurs end" },
      { tFromNow: -(3e5 * yearS),                           label: "Modern humans" },
      { tFromNow: 0,                                        label: "Now", emphasis: true },
      { tFromNow:  (5e9 * yearS),                           label: "Sun → red giant" },
      { tFromNow:  (1e14 * yearS),                          label: "Last stars die" },
    ];
    eras.forEach(e => {
      if (e.tFromNow < PAST_LIMIT_S || e.tFromNow > FUTURE_LIMIT_S) return;
      const x = xScale(e.tFromNow);
      root.append("line")
        .attr("x1", x).attr("x2", x).attr("y1", 0).attr("y2", innerH)
        .attr("stroke", e.emphasis ? "#444" : "#cfc8b3")
        .attr("stroke-dasharray", e.emphasis ? null : "3 3")
        .attr("stroke-width", e.emphasis ? 1.4 : 0.6);
      root.append("text").attr("x", x).attr("y", -8)
        .attr("text-anchor", "middle").attr("font-size", 9)
        .attr("fill", e.emphasis ? "#444" : "#888")
        .style("font-weight", e.emphasis ? 700 : 400)
        .text(e.label);
    });

    // ── Axes ────────────────────────────────────────────────────────────
    const xAxis = d3.axisBottom(xScale)
      .tickValues(visibleTicks)
      .tickFormat(d => formatTimeFromNow(d));
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
      .text("←  past  ·  time from now (symmetric log, 0 = present)  ·  future  →");
    root.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -innerH / 2).attr("y", -46)
      .attr("text-anchor", "middle").attr("fill", "#444")
      .attr("font-size", 12).attr("font-weight", 600)
      .text("density  →  log₁₀(ρ / kg·m⁻³)");

    // ── Universe trace ──────────────────────────────────────────────────
    // Each waypoint's x is "seconds from now", computed from its
    // time_after_bb_s. Anything pre-recombination (380 kyr after BB)
    // sits at essentially -universe_age within float precision and
    // gets stacked at the leftmost edge — that's accepted. The eye
    // wants resolution on the recent and the imminent, not on the
    // first picosecond.
    const universeObj = data.objects.find(o => o.id === "observable-universe");
    if (universeObj && universeObj.evolution) {
      const evo = universeObj.evolution
        .map(d => ({
          ...d,
          tFromNow: -(UNIVERSE_AGE_S - d.time_after_bb_s),
          y_log_d: Math.log10(d.density_kg_m3),
        }))
        .sort((a, b) => a.tFromNow - b.tFromNow);

      const lineGen = d3.line()
        .x(d => xScale(d.tFromNow))
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

      root.selectAll("circle.uni-evo").data(evo).join("circle")
        .attr("class", "uni-evo")
        .attr("cx", d => xScale(d.tFromNow))
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

    // ── All other objects (formed in the past, plotted at -age) ────────
    data.objects.forEach(obj => {
      if (obj.id === "observable-universe") return;
      if (!obj.formation || obj.formation.time_seconds_ago == null) return;
      const tFromNow = -obj.formation.time_seconds_ago;  // negative for past
      const d = obj.density_kg_m3;
      if (d <= 0) return;
      if (tFromNow < PAST_LIMIT_S || tFromNow > FUTURE_LIMIT_S) return;
      const y_log = Math.log10(d);
      if (y_log < yLogDomain[0] || y_log > yLogDomain[1]) return;
      const px = xScale(tFromNow);
      const py = yScale(y_log);
      const g = root.append("g")
        .attr("transform", `translate(${px},${py})`)
        .attr("data-id", obj.id)
        .style("cursor", "pointer");
      renderShape(g, obj, 4);
      g.on("mouseenter", e => { showTooltip(e, obj); crossChartHover(obj.id); })
       .on("mousemove", moveTooltip)
       .on("mouseleave", () => { hideTooltip(); crossChartClear(); });

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

  // Format a "seconds from now" tick into a human-readable label.
  // 0 = "now", negatives are past ("1 yr ago"), positives are future
  // ("1 yr from now"). Picks the largest unit that keeps the number
  // tidy (60 → "1 min", 3600 → "1 hr", etc.).
  function formatTimeFromNow(s) {
    if (s === 0) return "now";
    const past = s < 0;
    const a = Math.abs(s);
    let n, unit;
    if (a >= SECONDS_PER_YEAR * 1e9) { n = a / (SECONDS_PER_YEAR * 1e9); unit = "Gyr"; }
    else if (a >= SECONDS_PER_YEAR * 1e6) { n = a / (SECONDS_PER_YEAR * 1e6); unit = "Myr"; }
    else if (a >= SECONDS_PER_YEAR * 1e3) { n = a / (SECONDS_PER_YEAR * 1e3); unit = "kyr"; }
    else if (a >= SECONDS_PER_YEAR) { n = a / SECONDS_PER_YEAR; unit = "yr"; }
    else if (a >= 86400) { n = a / 86400; unit = "d"; }
    else if (a >= 3600)  { n = a / 3600; unit = "hr"; }
    else if (a >= 60)    { n = a / 60; unit = "min"; }
    else                 { n = a; unit = "s"; }
    const tidy = n >= 100 ? n.toFixed(0) : (n >= 10 ? n.toFixed(0) : n.toFixed(0));
    return past ? `${tidy} ${unit} ago` : `${tidy} ${unit} from now`;
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
      wireTourControls();
    } catch (e) {
      console.error("[universe] chart init failed:", e);
    }
  }

  function wireTourControls() {
    const startBtn = document.getElementById("uni-tour-button");
    if (startBtn) startBtn.addEventListener("click", startTour);
    const stopBtn = document.getElementById("uni-tour-stop");
    if (stopBtn) stopBtn.addEventListener("click", stopTour);
    const nextBtn = document.getElementById("uni-tour-next");
    if (nextBtn) nextBtn.addEventListener("click", () => { tourNext(); });
    const prevBtn = document.getElementById("uni-tour-prev");
    if (prevBtn) prevBtn.addEventListener("click", () => { tourPrev(); });
    document.addEventListener("keydown", e => {
      if (!tourActive) return;
      if (e.key === "Escape") stopTour();
      else if (e.key === "ArrowRight") tourNext();
      else if (e.key === "ArrowLeft") tourPrev();
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
