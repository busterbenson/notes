/**
 * clock13-horizon.js
 * Draws a curved horizon line on a canvas overlay, dividing the clock
 * into sky (above) and ground (below).  The curve is a quadratic bezier
 * that always passes through the center of the clock.
 *
 * The ground color is a darker, warmer version of the current
 * sky/background color (Strategy C).
 *
 * Dependencies: ClockConfig (for COLORS), ClockAstro (for posMod)
 */

var ClockHorizon = (function (Config, Astro) {
  'use strict';

  // ─── Configuration ────────────────────────────────────────────
  // Ground fill opacity
  var GROUND_OPACITY = 0.65;

  // Horizon line opacity
  var LINE_OPACITY = 0.4;

  // How much to darken + warm the sky color for ground
  var DARKEN_R = 0.35;
  var DARKEN_G = 0.30;
  var DARKEN_B = 0.25;
  var WARM_R = 15;
  var WARM_G = 8;
  var WARM_B = 0;

  // Line color multipliers (brighter than ground)
  var LINE_R = 0.6;
  var LINE_G = 0.5;
  var LINE_B = 0.4;
  var LINE_WARM_R = 30;
  var LINE_WARM_G = 20;
  var LINE_WARM_B = 10;

  // ─── Helpers ──────────────────────────────────────────────────
  function degToRad(d) {
    return d * Math.PI / 180;
  }

  function normalizeAngle(a) {
    return ((a % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
  }

  /**
   * Parse an rgb/hex color string into [r, g, b].
   */
  function parseColor(color) {
    if (!color) return [17, 34, 102];

    var rgbMatch = color.match(/rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)/);
    if (rgbMatch) {
      return [parseInt(rgbMatch[1]), parseInt(rgbMatch[2]), parseInt(rgbMatch[3])];
    }

    if (color.charAt(0) === '#' && color.length === 7) {
      return [
        parseInt(color.slice(1, 3), 16),
        parseInt(color.slice(3, 5), 16),
        parseInt(color.slice(5, 7), 16)
      ];
    }

    return [17, 34, 102];
  }

  function groundColorFromSky(skyRGB) {
    return [
      Math.round(Math.min(255, skyRGB[0] * DARKEN_R + WARM_R)),
      Math.round(Math.min(255, skyRGB[1] * DARKEN_G + WARM_G)),
      Math.round(Math.min(255, skyRGB[2] * DARKEN_B + WARM_B))
    ];
  }

  function lineColorFromSky(skyRGB) {
    return [
      Math.round(Math.min(255, skyRGB[0] * LINE_R + LINE_WARM_R)),
      Math.round(Math.min(255, skyRGB[1] * LINE_G + LINE_WARM_G)),
      Math.round(Math.min(255, skyRGB[2] * LINE_B + LINE_WARM_B))
    ];
  }

  function rgba(rgb, a) {
    return 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',' + a + ')';
  }

  // ─── State for resize redraw ───────────────────────────────────
  var lastParams = null;

  // ─── Main render ──────────────────────────────────────────────
  function render(sunriseAngle, sunsetAngle, skyColor) {
    lastParams = { sunriseAngle: sunriseAngle, sunsetAngle: sunsetAngle, skyColor: skyColor };

    var canvas = document.getElementById('horizon-canvas');
    if (!canvas) return;

    var container = canvas.parentElement;
    if (!container) return;

    var w = container.offsetWidth;
    var h = container.offsetHeight;
    if (w === 0 || h === 0) return;

    var dpr = window.devicePixelRatio || 1;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';

    var ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    var cx = w / 2;
    var cy = h / 2;
    var radius = Math.min(cx, cy);

    // Parse colors
    var skyRGB = parseColor(skyColor);
    var groundRGB = groundColorFromSky(skyRGB);
    var lineRGB = lineColorFromSky(skyRGB);

    // ─── Compute sunrise/sunset positions on the circle edge ─────
    // Clock: 0° = top, clockwise.  Canvas: 0° = right, counter-clockwise.
    var srRad = degToRad(sunriseAngle - 90);
    var ssRad = degToRad(sunsetAngle - 90);

    var srX = cx + radius * Math.cos(srRad);
    var srY = cy + radius * Math.sin(srRad);
    var ssX = cx + radius * Math.cos(ssRad);
    var ssY = cy + radius * Math.sin(ssRad);

    // ─── Quadratic bezier through the clock center ──────────────
    // For a quadratic bezier from P0 to P2 with control point P1,
    // the point at t=0.5 is:  Q = (P0 + 2*P1 + P2) / 4
    //
    // Setting Q = (cx, cy) and solving for P1:
    //   P1 = 2*(cx,cy) - (P0 + P2)/2
    //
    // This guarantees the curve passes through the exact center.

    var midX = (srX + ssX) / 2;   // midpoint of the chord
    var midY = (srY + ssY) / 2;

    var cpX = 2 * cx - midX;      // control point
    var cpY = 2 * cy - midY;

    // ─── Determine nighttime arc direction ──────────────────────
    // The ground fill needs a circle arc from sunset back to sunrise
    // going through midnight (the nighttime side).
    //
    // Midnight on this clock is at clock-degree 180° → canvas angle
    // = 180° − 90° = 90° = PI/2.  We pick whichever arc direction
    // (clockwise or counter-clockwise) passes through midnight.

    var midnightRad = Math.PI / 2;

    // Sweep counter-clockwise (positive direction) from ssRad:
    // how far to midnight vs how far to srRad?
    var ccwToMidnight = normalizeAngle(midnightRad - ssRad);
    var ccwToSunrise  = normalizeAngle(srRad - ssRad);

    // If midnight is encountered before sunrise going CCW,
    // then CCW is the nighttime direction → anticlockwise = true
    var nightArcCCW = (ccwToMidnight >= ccwToSunrise);

    // ─── Ground fill ────────────────────────────────────────────
    ctx.save();
    ctx.beginPath();

    // 1. Bezier from sunrise → sunset (the horizon curve through center)
    ctx.moveTo(srX, srY);
    ctx.quadraticCurveTo(cpX, cpY, ssX, ssY);

    // 2. Circle arc from sunset → sunrise through the nighttime side
    ctx.arc(cx, cy, radius, ssRad, srRad, nightArcCCW);

    ctx.closePath();
    ctx.fillStyle = rgba(groundRGB, GROUND_OPACITY);
    ctx.fill();
    ctx.restore();

    // ─── Horizon line (the bezier stroke) ────────────────────────
    ctx.save();

    // Clip to circle so the line stays inside
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.clip();

    ctx.beginPath();
    ctx.moveTo(srX, srY);
    ctx.quadraticCurveTo(cpX, cpY, ssX, ssY);
    ctx.strokeStyle = rgba(lineRGB, LINE_OPACITY);
    ctx.lineWidth = Math.max(1, radius / 120);
    ctx.stroke();
    ctx.restore();
  }

  function redraw() {
    if (lastParams) {
      render(lastParams.sunriseAngle, lastParams.sunsetAngle, lastParams.skyColor);
    }
  }

  // ─── Public API ───────────────────────────────────────────────
  return {
    render: render,
    redraw: redraw
  };

})(ClockConfig, ClockAstro);
