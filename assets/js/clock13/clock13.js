/**
 * clock13.js
 * Main orchestrator for the Quirky Clock.
 * Wires up events, manages state, runs the update pipeline.
 *
 * Dependencies: jQuery ($), moment, ClockConfig, ClockAstro, ClockRender
 *
 * Usage (from the layout):
 *   ClockApp.init({ apiUserId: '...', apiKey: '...' });
 */

var ClockApp = (function ($, moment, Config, Astro, Render) {
  'use strict';

  // ─── Internal State ──────────────────────────────────────────────
  var state = {
    debug: false,
    dataControls: false,
    timeInputType: 'auto', // 'auto' | 'manual'
    lat: null,
    lng: null,
    locationCached: false,  // true once we have a valid lat/lng
    now: null,            // Date object for the currently displayed time
    currentTimeDeg: null, // current time as dial degrees
    timezoneOffset: null, // hours offset from UTC (e.g., -8 for PST)
    seasonalData: null,   // from ClockAstro.getSeasonalData
    planets: null,        // from ClockAstro.getPlanetaryPositions
    plotResult: null,     // from ClockAstro.computePlotPositions
    apiUserId: null,
    apiKey: null,
    refreshTimer: null,
    currentXHR: null         // reference to in-flight API call (for cancellation)
  };

  // ─── Initialization ──────────────────────────────────────────────
  function init(options) {
    options = options || {};
    state.apiUserId = options.apiUserId || '';
    state.apiKey = options.apiKey || '';
    state.debug = options.debug || false;
    state.dataControls = options.dataControls || false;

    // Toggle debug/data sections
    state.debug ? $('#debug').show() : $('#debug').hide();
    state.dataControls ? $('#moonth-data').show() : $('#moonth-data').hide();

    // Wire up events
    wireEvents();

    // Start
    $(window).on('resize', Render.scaleClockToSquare);
    requestUpdate();
  }

  // ─── Event Wiring ────────────────────────────────────────────────
  function wireEvents() {
    // Initial load button
    $('#get-location-link').on('click', function (e) {
      e.preventDefault();
      state.locationCached = false; // force re-request on manual retry
      requestUpdate();
    });

    // Manual date/time entry
    $('#date-and-time').on('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        state.timeInputType = 'manual';
        requestUpdate();
      }
    });

    // Navigation links (attach to <a> inside the span via delegation)
    $('#prev-day a, #prev-day').on('click', function (e) { e.preventDefault(); shiftTime(-1, 'day'); });
    $('#prev-hour a, #prev-hour').on('click', function (e) { e.preventDefault(); shiftTime(-1, 'hour'); });
    $('#right-now a, #right-now').on('click', function (e) {
      e.preventDefault();
      $('#date-and-time').val('');
      state.timeInputType = 'auto';
      requestUpdate();
    });
    $('#this-sunset a, #this-sunset').on('click', function (e) {
      e.preventDefault();
      if (state.seasonalData && state.seasonalData.sunset) {
        $('#date-and-time').val(state.seasonalData.sunset);
        state.timeInputType = 'manual';
        requestUpdate();
      }
    });
    $('#next-hour a, #next-hour').on('click', function (e) { e.preventDefault(); shiftTime(1, 'hour'); });
    $('#next-day a, #next-day').on('click', function (e) { e.preventDefault(); shiftTime(1, 'day'); });

    // Show/hide controls
    $('#show-controls').on('click', function (e) { e.preventDefault(); Render.showControls(); });
    $('#hide-controls').on('click', function (e) { e.preventDefault(); Render.hideControls(); });

    // Show/hide planet hands
    var planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'];
    for (var i = 0; i < planets.length; i++) {
      (function (token) {
        $('#show-' + token).on('change', function () { Render.toggleHand(token); });
      })(planets[i]);
    }

    // Save data row
    $('#save-moonth-data-row').on('click', function (e) {
      e.preventDefault();
      if (state.plotResult) {
        Render.appendMoonthDataRow(state);
      }
    });
  }

  // ─── Time Navigation ─────────────────────────────────────────────
  function shiftTime(amount, unit) {
    var val = $('#date-and-time').val();
    var ts = Date.parse(val);
    if (isNaN(ts)) return;

    var d = new Date(ts);
    if (unit === 'day') {
      d.setDate(d.getDate() + amount);
    } else if (unit === 'hour') {
      d.setHours(d.getHours() + amount);
    }
    $('#date-and-time').val(d);
    state.timeInputType = 'manual';
    requestUpdate();
  }

  // ─── Configure Time ──────────────────────────────────────────────
  function configureTime() {
    if (state.timeInputType === 'manual') {
      var val = $('#date-and-time').val();
      if (val && val.trim().length > 0) {
        var ts = Date.parse(val);
        if (!isNaN(ts)) {
          state.now = new Date(ts);
        } else {
          // Invalid input → fall back to now
          state.now = new Date();
          state.timeInputType = 'auto';
        }
      } else {
        state.now = new Date();
        state.timeInputType = 'auto';
      }
    } else {
      state.now = new Date();
    }

    state.currentTimeDeg = Astro.dateToTimeDegrees(state.now);
    state.timezoneOffset = -state.now.getTimezoneOffset() / 60;

    // Update the input to show current time
    Render.updateDateInput(state.now);
  }

  // ─── Main Update Pipeline ────────────────────────────────────────
  function requestUpdate() {
    // Cancel any pending auto-refresh
    if (state.refreshTimer) {
      clearTimeout(state.refreshTimer);
      state.refreshTimer = null;
    }

    // If we already have cached coordinates, skip geolocation on auto-refresh
    if (state.locationCached && state.lat !== null && state.lng !== null) {
      runUpdatePipeline(state.lat, state.lng);
      return;
    }

    // First time: request geolocation
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function (pos) {
          state.lat = pos.coords.latitude;
          state.lng = pos.coords.longitude;
          state.locationCached = true;
          $('#location-status').hide();
          runUpdatePipeline(state.lat, state.lng);
        },
        function (err) {
          console.warn('Geolocation error:', err.message);
          $('#location-status').html(
            'Location unavailable. <a href="#" id="get-location-link">Click to retry</a>, or using default (Oakland, CA).'
          );
          // Re-wire the retry link
          $('#get-location-link').on('click', function (e) {
            e.preventDefault();
            state.locationCached = false;
            requestUpdate();
          });
          // Use default location
          state.lat = Config.DEFAULT_LOCATION.lat;
          state.lng = Config.DEFAULT_LOCATION.lng;
          state.locationCached = true;
          $('#location-status').hide();
          runUpdatePipeline(state.lat, state.lng);
        },
        { timeout: 10000 } // 10s timeout for geolocation
      );
    } else {
      // No geolocation API → use default
      state.lat = Config.DEFAULT_LOCATION.lat;
      state.lng = Config.DEFAULT_LOCATION.lng;
      state.locationCached = true;
      runUpdatePipeline(state.lat, state.lng);
    }
  }

  // ─── Core Update Pipeline (called after location is resolved) ────
  function runUpdatePipeline(lat, lng) {
    // Abort any in-flight API call from a previous update
    if (state.currentXHR && state.currentXHR.abort) {
      state.currentXHR.abort();
      state.currentXHR = null;
    }

    // Configure what time we're displaying
    configureTime();

    // 1. Get seasonal data (sunrise, sunset, moon — via SunCalc, instant)
    state.seasonalData = Astro.getSeasonalData(lat, lng, state.now);
    Render.updateSunsetTimeDisplay(state.seasonalData.sunsetTimeStr);

    // 2. Get planetary positions (via API, async)
    if (!state.apiUserId || !state.apiKey) {
      console.warn('Astrology API credentials not configured. Planet positions will be estimated.');
    }
    state.currentXHR = Astro.getPlanetaryPositions(
      state.now,
      state.currentTimeDeg,
      lat,
      lng,
      state.timezoneOffset,
      state.apiUserId,
      state.apiKey
    );
    state.currentXHR.then(function (planets) {
      if (planets && planets.length > 0) {
        state.planets = planets;
      } else if (!state.planets || state.planets.length === 0) {
        // No cached data either — create minimal fallback
        console.warn('No planetary data received. Clock will show sun/moon only.');
        var doy = Astro.dayOfYear(state.now);
        var sunLongitude = Astro.posMod((doy - 80) * (360 / 365.25), 360);
        state.planets = [{ name: 'Sun', token: 'sun', eclipticLongitude: sunLongitude, isRetrograde: false }];
      }
      // else: keep the last good state.planets data

      renderFromState();

    }).catch(function (err) {
      console.error('Clock update error:', err);

      // Fall back to last good planet data if available
      if (!state.planets || state.planets.length === 0) {
        var doy = Astro.dayOfYear(state.now);
        var sunLongitude = Astro.posMod((doy - 80) * (360 / 365.25), 360);
        state.planets = [{ name: 'Sun', token: 'sun', eclipticLongitude: sunLongitude, isRetrograde: false }];
      }

      // Still render with whatever data we have
      renderFromState();
    });
  }

  // ─── Render from current state ───────────────────────────────────
  function renderFromState() {
    try {
      // Compute plot positions (pure math, instant)
      state.plotResult = Astro.computePlotPositions(
        state.seasonalData,
        state.planets,
        state.currentTimeDeg
      );

      // Render everything
      Render.scaleClockToSquare();
      Render.renderClock(state.plotResult, state.seasonalData.moon);
      Render.renderDebugInfo(state);
    } catch (e) {
      console.error('Clock render error:', e);
    }

    state.currentXHR = null;

    // Schedule next auto-refresh
    scheduleNextRefresh();
  }

  // ─── Schedule the next auto-refresh ──────────────────────────────
  function scheduleNextRefresh() {
    if (state.timeInputType === 'auto') {
      state.refreshTimer = setTimeout(requestUpdate, Config.AUTO_REFRESH_MS);
    }
  }

  // ─── Public API ──────────────────────────────────────────────────
  return {
    init: init
  };

})(jQuery, moment, ClockConfig, ClockAstro, ClockRender);
