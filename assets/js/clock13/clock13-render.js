/**
 * clock13-render.js
 * DOM rendering for the Quirky Clock.
 * All jQuery / DOM manipulation lives here.
 *
 * Dependencies: jQuery ($), ClockConfig, ClockAstro (for utility fns)
 */

var ClockRender = (function ($, Config, Astro) {
  'use strict';

  // ─── Cumulative rotation tracking ─────────────────────────────────
  // Stores the last applied rotation (in unbounded degrees) for each
  // element ID so we can always take the shortest-path rotation and
  // avoid the 360° wrap-around jump.
  var lastRotation = {};
  var firstRenderDone = false;

  /**
   * Given a target angle (0-360) and the element's last cumulative angle,
   * return a new cumulative angle that is equivalent mod 360 but takes
   * the shortest path from the previous angle.
   */
  function smoothAngle(elementKey, targetDeg) {
    if (!(elementKey in lastRotation)) {
      // First render — just use the raw angle, no transition needed
      lastRotation[elementKey] = targetDeg;
      return targetDeg;
    }

    var prev = lastRotation[elementKey];
    // Normalize target to 0-360
    targetDeg = ((targetDeg % 360) + 360) % 360;

    // Find the equivalent target closest to the previous value
    // by computing the shortest angular difference
    var diff = targetDeg - (((prev % 360) + 360) % 360);
    if (diff > 180) diff -= 360;
    if (diff < -180) diff += 360;

    var result = prev + diff;
    lastRotation[elementKey] = result;
    return result;
  }

  // ─── Scale the clock to be a square (viewport-aware) ────────────
  function scaleClockToSquare() {
    var canvas = $('#clock-canvas');
    // The actual rendered size of the canvas (CSS already constrains it)
    var size = canvas.width();
    $('#clock').css('height', size);
    canvas.css('height', size);
  }

  // ─── Render all planet and moon hands ────────────────────────────
  /**
   * @param {Object} result - from ClockAstro.computePlotPositions()
   *   result.plots      — { sun: {...}, moon: {...}, mercury: {...}, ... }
   *   result.handOrder  — ['moon', 'mercury', 'sun', 'venus', ...]
   *   result.moments    — { sunrise: {degrees}, sunset: {degrees}, solarNoon: {degrees} }
   *   result.constellations — { degrees }
   * @param {Object} moonData - seasonalData.moon (for phase name)
   */
  function renderClock(result, moonData) {
    renderMomentHands(result.moments, result.constellations);
    renderPlanetHands(result.plots, result.handOrder, moonData);
    renderBackground(result.plots.sun.degrees,
                     result.moments.sunrise.degrees,
                     result.moments.sunset.degrees);

    // Draw the elliptical horizon overlay
    var skyColor = $('#clock-canvas').css('background-color');
    if (typeof ClockHorizon !== 'undefined') {
      ClockHorizon.render(
        result.moments.sunrise.degrees,
        result.moments.sunset.degrees,
        skyColor
      );
    }

    // After the first render, enable CSS transitions for smooth updates
    if (!firstRenderDone) {
      firstRenderDone = true;
      // Use requestAnimationFrame to ensure the first paint completes
      // before enabling transitions, so hands snap into place first
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          var handSelector = '#hand-1, #hand-2, #hand-3, #hand-4, #hand-5, ' +
            '#hand-6, #hand-7, #hand-8, #hand-9, #hand-10, ' +
            '#hand-sunrise, #hand-sunset, #hand-constellations, ' +
            '#label-hand-1, #label-hand-2, #label-hand-3, #label-hand-4, #label-hand-5, ' +
            '#label-hand-6, #label-hand-7, #label-hand-8, #label-hand-9, #label-hand-10';
          $(handSelector).css('transition', 'transform 1s ease-in-out');
        });
      });
    }
  }

  // ─── Render sunrise / sunset / constellation hands ───────────────
  function renderMomentHands(moments, constellations) {
    // Sunrise hand
    var sunriseAngle = smoothAngle('hand-sunrise', moments.sunrise.degrees);
    $('#hand-sunrise')
      .css('background-image', "url('" + Config.IMAGE_BASE + "/v2/sun/sunrise.png')")
      .css('transform', 'rotate(' + Math.round(sunriseAngle) + 'deg)')
      .css('z-index', 50);

    // Sunset hand (same image, different angle)
    var sunsetAngle = smoothAngle('hand-sunset', moments.sunset.degrees);
    $('#hand-sunset')
      .css('background-image', "url('" + Config.IMAGE_BASE + "/v2/sun/sunrise.png')")
      .css('transform', 'rotate(' + Math.round(sunsetAngle) + 'deg)')
      .css('z-index', 50);

    // Constellations ring (behind everything else, but still above clock bg)
    var constAngle = smoothAngle('hand-constellations', constellations.degrees);
    $('#hand-constellations')
      .css('background-image', "url('" + Config.IMAGE_BASE + "/v2/constellations.png')")
      .css('transform', 'rotate(' + Math.round(constAngle) + 'deg)')
      .css('z-index', 2)
      .css('opacity', 0.8);
  }

  // ─── Render planet hands (rotation + images) ─────────────────────
  function renderPlanetHands(plots, handOrder, moonData) {
    var order = 1;

    for (var i = 0; i < handOrder.length; i++) {
      var token = handOrder[i];
      var plot = plots[token];
      if (!plot) continue;

      var handId = '#hand-' + order;
      var labelId = '#label-hand-' + order;

      // Set data attribute for show/hide toggling
      $(handId).attr('v-planet', token);
      $(labelId).attr('v-planet-label', token);

      // Choose image
      var imagePath;
      if (token === 'moon' && moonData) {
        var phaseImg = Config.MOON_PHASE_IMAGES[moonData.phaseName] || 'v2/moon/full/moon';
        imagePath = Config.IMAGE_BASE + '/' + phaseImg + '_' + plot.line + '.png';
      } else {
        // Find the planet config for the image path
        var planetConfig = findPlanetConfig(token);
        var basePath = planetConfig ? planetConfig.imagePath : 'v2/planets/planets';
        imagePath = Config.IMAGE_BASE + '/' + basePath + '_' + plot.line + '.png';
      }

      var handKey = 'hand-' + order;
      var labelKey = 'label-hand-' + order;
      var angle = smoothAngle(handKey, plot.degrees);
      var rotateStr = 'rotate(' + Math.round(angle) + 'deg)';

      $(handId)
        .css('background-image', "url('" + imagePath + "')")
        .css('transform', rotateStr)
        .css('z-index', 100 - order);

      // Labels for planets (not sun or moon)
      var planetConfig = findPlanetConfig(token);
      if (planetConfig && planetConfig.hasLabel) {
        var labelAngle = smoothAngle(labelKey, plot.degrees);
        $(labelId)
          .css('background-image', "url('" + Config.IMAGE_BASE + "/v2/planets/" + token + "-label.png')")
          .css('transform', 'rotate(' + Math.round(labelAngle) + 'deg)')
          .css('z-index', 10)
          .css('opacity', 0.7);
      }

      order++;
    }
  }

  function findPlanetConfig(token) {
    for (var i = 0; i < Config.PLANETS.length; i++) {
      if (Config.PLANETS[i].token === token) return Config.PLANETS[i];
    }
    return null;
  }

  // ─── Background color based on sun position ──────────────────────
  function renderBackground(sunAngle, sunriseAngle, sunsetAngle) {
    var color = computeBackgroundColor(sunAngle, sunriseAngle, sunsetAngle);
    // Apply sky color to the clock circle only (not the page body)
    $('#clock-canvas').css('background-color', color);
  }

  function computeBackgroundColor(sunAngle, sunriseAngle, sunsetAngle) {
    var C = Config.COLORS;
    var T = Config.TWILIGHT_DEGREES;

    // Compute the noon angle as the midpoint between sunrise and sunset on the clock
    var noonAngle = Astro.posMod((sunriseAngle + sunsetAngle) / 2, 360);
    // If sunrise is > sunset on the dial (wraps around), the midpoint is the other way
    if (sunriseAngle > sunsetAngle) {
      noonAngle = Astro.posMod(noonAngle + 180, 360);
    }

    // Pre-sunrise glow
    if (isBetween(sunAngle, sunriseAngle - T, sunriseAngle)) {
      return interpolateColor(C.dawn, C.preSunrise, (sunAngle - (sunriseAngle - T)) / T);
    }
    // Post-sunrise warmth
    if (isBetween(sunAngle, sunriseAngle, sunriseAngle + T)) {
      return interpolateColor(C.preSunrise, C.postSunrise, (sunAngle - sunriseAngle) / T);
    }
    // Morning → noon
    if (isBetween(sunAngle, sunriseAngle + T, noonAngle)) {
      var morningSpan = Astro.posMod(noonAngle - (sunriseAngle + T), 360);
      return interpolateColor(C.sunrise, C.noon, Astro.posMod(sunAngle - (sunriseAngle + T), 360) / morningSpan);
    }
    // Noon → pre-sunset
    if (isBetween(sunAngle, noonAngle, sunsetAngle - T)) {
      var afternoonSpan = Astro.posMod((sunsetAngle - T) - noonAngle, 360);
      return interpolateColor(C.noon, C.sunset, Astro.posMod(sunAngle - noonAngle, 360) / afternoonSpan);
    }
    // Pre-sunset glow
    if (isBetween(sunAngle, sunsetAngle - T, sunsetAngle)) {
      return interpolateColor(C.sunset, C.preSunset, (sunAngle - (sunsetAngle - T)) / T);
    }
    // Post-sunset warmth
    if (isBetween(sunAngle, sunsetAngle, sunsetAngle + T)) {
      return interpolateColor(C.preSunset, C.postSunset, (sunAngle - sunsetAngle) / T);
    }
    // Night (everything else)
    return C.night;
  }

  /**
   * Check if angle is between start and end on a circular dial.
   * Handles wrap-around (e.g., start=350, end=10).
   */
  function isBetween(angle, start, end) {
    start = Astro.posMod(start, 360);
    end   = Astro.posMod(end, 360);
    angle = Astro.posMod(angle, 360);
    if (start <= end) {
      return angle >= start && angle <= end;
    }
    return angle >= start || angle <= end;
  }

  /**
   * Linearly interpolate between two hex colors.
   * factor: 0 = color1, 1 = color2
   */
  function interpolateColor(color1, color2, factor) {
    factor = Math.max(0, Math.min(1, factor)); // clamp

    var r1 = parseInt(color1.slice(1, 3), 16);
    var g1 = parseInt(color1.slice(3, 5), 16);
    var b1 = parseInt(color1.slice(5, 7), 16);
    var r2 = parseInt(color2.slice(1, 3), 16);
    var g2 = parseInt(color2.slice(3, 5), 16);
    var b2 = parseInt(color2.slice(5, 7), 16);

    var r = Math.round(r1 + (r2 - r1) * factor);
    var g = Math.round(g1 + (g2 - g1) * factor);
    var b = Math.round(b1 + (b2 - b1) * factor);

    return 'rgb(' + r + ', ' + g + ', ' + b + ')';
  }

  // ─── Debug panel ─────────────────────────────────────────────────
  function renderDebugInfo(state) {
    if (!state.debug) return;
    $('#debug').show();

    var sd = state.seasonalData;
    var plots = state.plotResult.plots;
    var moments = state.plotResult.moments;

    $('#date').html(sd.date);
    $('#current_time').html(Astro.degreesToTimeString(state.currentTimeDeg));
    $('#aries_relative_to_year').html(
      Number(state.plotResult.ariesRelative * 100 / 360).toFixed(2) + '%'
    );

    // Sun
    var sunPlot = plots.sun;
    $('#sun_debug').html(
      Astro.degreesToTimeString(sunPlot.degrees) + '🕰️, ' +
      Number(sunPlot.degrees).toFixed(2) + '°' +
      (sunPlot.isAboveHorizon ? ', visible' : '') +
      ', line ' + sunPlot.line
    );
    $('#sunrise_debug').html(sd.sunriseTimeStr + '🕰️, ' + Number(moments.sunrise.degrees).toFixed(2) + '°');
    $('#highnoon_debug').html(sd.solarNoonTimeStr + '🕰️, ' + Number(moments.solarNoon.degrees).toFixed(2) + '°');
    $('#sunset_debug').html(sd.sunsetTimeStr + '🕰️, ' + Number(moments.sunset.degrees).toFixed(2) + '°');

    // Moon
    var moonPlot = plots.moon;
    if (moonPlot) {
      $('#moon_debug').html(
        Astro.degreesToTimeString(moonPlot.degrees) + '🕰️, ' +
        Number(moonPlot.degrees).toFixed(2) + '°' +
        (moonPlot.isAboveHorizon ? ', above horizon' : '') +
        (moonPlot.isVisible ? ', visible' : '') +
        ', line ' + moonPlot.line
      );
      $('#moon_phase_rough_debug').html(sd.moon.phaseName);
      $('#moon_status_debug').html(sd.moon.isWaxing ? 'Waxing' : 'Waning');
      $('#moon_illumination_debug').html(sd.moon.illuminationPct + '%');
      $('#moon_parallactic_angle_debug').html(Number(sd.moon.parallacticAngle).toFixed(2) + '°');
    }

    // Planets
    var planetTokens = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'];
    for (var i = 0; i < planetTokens.length; i++) {
      var t = planetTokens[i];
      var p = plots[t];
      if (p) {
        $('#' + t + '_debug').html(
          Astro.degreesToTimeString(p.degrees) + '🕰️, ' +
          Number(p.degrees).toFixed(2) + '°' +
          (p.isAboveHorizon ? ', above horizon' : '') +
          (p.isVisible ? ', visible' : '') +
          ', line ' + p.line
        );
      }
    }
  }

  // ─── Moonth data table ───────────────────────────────────────────
  function appendMoonthDataRow(state) {
    var sd = state.seasonalData;
    var plots = state.plotResult.plots;
    var row = $('<tr>');
    row.append($('<td>').text(sd.date));
    row.append($('<td>').text(sd.sunsetTimeStr));

    var bodies = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'];
    for (var i = 0; i < bodies.length; i++) {
      var p = plots[bodies[i]];
      row.append($('<td>').text(p ? Number(p.degrees).toFixed(1) : '--'));
    }
    $('#moonth-data-table').append(row);
  }

  // ─── Controls visibility ─────────────────────────────────────────
  function showControls() {
    $('#hidden-date-links').hide();
    $('#visible-date-links').show();
    $('#clock-preferences').show();
  }

  function hideControls() {
    $('#hidden-date-links').show();
    $('#visible-date-links').hide();
    $('#clock-preferences').hide();
  }

  // ─── Show / hide individual planet hand ──────────────────────────
  function toggleHand(token) {
    var hand = $("[v-planet='" + token + "']");
    var label = $("[v-planet-label='" + token + "']");
    hand.toggleClass('hidden');
    label.toggleClass('hidden');
  }

  // ─── Update the date/time display ────────────────────────────────
  function updateDateInput(date) {
    if (!(date instanceof Date)) date = new Date(date);

    var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    var months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December'];

    var h = date.getHours();
    var m = date.getMinutes();
    var ampm = h >= 12 ? 'pm' : 'am';
    var h12 = h % 12 || 12;
    var mm = m < 10 ? '0' + m : m;

    var formatted = days[date.getDay()] + ', '
      + months[date.getMonth()] + ' ' + date.getDate() + ', '
      + date.getFullYear()
      + '  ·  ' + h12 + ':' + mm + ' ' + ampm;

    $('#date-and-time').val(formatted);
    // Store the real Date object so the input can still be edited
    $('#date-and-time').data('rawDate', date);
  }

  function updateSunriseTimeDisplay(timeStr) {
    $('#time_of_sunrise').html(timeStr);
  }

  function updateSunsetTimeDisplay(timeStr) {
    $('#time_of_sunset').html(timeStr);
  }

  // ─── Public API ──────────────────────────────────────────────────
  return {
    scaleClockToSquare: scaleClockToSquare,
    renderClock: renderClock,
    renderDebugInfo: renderDebugInfo,
    appendMoonthDataRow: appendMoonthDataRow,
    showControls: showControls,
    hideControls: hideControls,
    toggleHand: toggleHand,
    updateDateInput: updateDateInput,
    updateSunriseTimeDisplay: updateSunriseTimeDisplay,
    updateSunsetTimeDisplay: updateSunsetTimeDisplay
  };

})(jQuery, ClockConfig, ClockAstro);
