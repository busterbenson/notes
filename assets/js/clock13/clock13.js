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
    lastRefreshTime: null,   // timestamp of the last successful refresh (for drift detection)
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
    $(window).on('resize', function () {
      Render.scaleClockToSquare();
      if (typeof ClockHorizon !== 'undefined') {
        ClockHorizon.redraw();
      }
    });
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
        // Clear cached date so configureTime parses the input text
        state.now = null;
        $('#date-and-time').data('rawDate', null);
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
    $('#this-sunrise a, #this-sunrise').on('click', function (e) {
      e.preventDefault();
      if (state.seasonalData && state.seasonalData.sunrise) {
        state.now = new Date(state.seasonalData.sunrise.getTime());
        state.timeInputType = 'manual';
        requestUpdate();
      }
    });
    $('#this-sunset a, #this-sunset').on('click', function (e) {
      e.preventDefault();
      if (state.seasonalData && state.seasonalData.sunset) {
        state.now = new Date(state.seasonalData.sunset.getTime());
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
    // Use the stored raw Date object (the formatted display string isn't parseable)
    var d = $('#date-and-time').data('rawDate');
    if (!d || !(d instanceof Date)) {
      d = state.now || new Date();
    }
    d = new Date(d.getTime()); // clone so we don't mutate

    if (unit === 'day') {
      d.setDate(d.getDate() + amount);
    } else if (unit === 'hour') {
      d.setHours(d.getHours() + amount);
    }
    // Store the new date so the next shift works too
    $('#date-and-time').data('rawDate', d);
    state.timeInputType = 'manual';
    state.now = d;
    requestUpdate();
  }

  // ─── Parse user-entered date string ──────────────────────────────
  function parseUserDate(val) {
    if (!val || !val.trim()) return null;

    // Try native Date.parse first (handles many formats)
    var ts = Date.parse(val);
    if (!isNaN(ts)) return new Date(ts);

    // Handle our formatted display: "Friday, March 13, 2026  ·  12:08 am"
    // Strip day name and the · separator, normalize whitespace
    var cleaned = val
      .replace(/^[A-Za-z]+,\s*/, '')   // remove "Friday, "
      .replace(/\s*·\s*/g, ' ')         // replace · with space
      .trim();
    // Now we have something like "March 13, 2026 12:08 am"
    ts = Date.parse(cleaned);
    if (!isNaN(ts)) return new Date(ts);

    // Try moment.js as a last resort
    if (typeof moment !== 'undefined') {
      var m = moment(val, [
        'MMMM D, YYYY h:mm a',
        'MMMM D, YYYY h:mma',
        'MMM D, YYYY h:mm a',
        'YYYY-MM-DD HH:mm',
        'YYYY-MM-DD',
        'MM/DD/YYYY',
        'M/D/YYYY'
      ]);
      if (m.isValid()) return m.toDate();
    }

    return null;
  }

  // ─── Configure Time ──────────────────────────────────────────────
  function configureTime() {
    if (state.timeInputType === 'manual') {
      // Prefer the already-set state.now (from shiftTime / sunrise / sunset click),
      // then fall back to the stored raw date, then try parsing the input.
      if (state.now && state.now instanceof Date && !isNaN(state.now.getTime())) {
        // already set — use it
      } else {
        var raw = $('#date-and-time').data('rawDate');
        if (raw && raw instanceof Date) {
          state.now = raw;
        } else {
          var parsed = parseUserDate($('#date-and-time').val());
          if (parsed) {
            state.now = parsed;
          } else {
            state.now = new Date();
            state.timeInputType = 'auto';
          }
        }
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
    Render.updateSunriseTimeDisplay(state.seasonalData.sunriseTimeStr);
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
      } else {
        // API returned empty — use local orbital estimates for the current date
        console.warn('No planetary data from API. Using local orbital estimates.');
        state.planets = Astro.estimatePlanetaryPositions(state.now);
      }

      renderFromState();

    }).catch(function (err) {
      console.error('Clock update error:', err);

      // API failed — use local orbital estimates for the current date
      // (always re-estimate so positions match the displayed date, not a stale one)
      state.planets = Astro.estimatePlanetaryPositions(state.now);

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
      state.lastRefreshTime = Date.now();
      state.refreshTimer = setTimeout(function () {
        // Drift detection: if the timer fires much later than expected
        // (e.g. browser throttled the tab, or device slept), log it.
        // Either way, we update — the important thing is the timer keeps running.
        var elapsed = Date.now() - state.lastRefreshTime;
        if (elapsed > Config.AUTO_REFRESH_MS * 1.5) {
          console.info('Clock: timer drifted (' + Math.round(elapsed / 1000) + 's elapsed, expected ' + Math.round(Config.AUTO_REFRESH_MS / 1000) + 's). Catching up.');
        }
        requestUpdate();
      }, Config.AUTO_REFRESH_MS);
    }
  }

  // ─── Visibility & Focus Recovery ──────────────────────────────────
  // Browsers throttle or pause setTimeout in background tabs and after
  // sleep/wake. These listeners ensure the clock recovers immediately
  // when the user returns, AND that the timer chain is always re-established
  // even if setTimeout silently died.

  function ensureTimerAlive() {
    if (state.timeInputType !== 'auto') return;

    var now = Date.now();
    var elapsed = state.lastRefreshTime ? (now - state.lastRefreshTime) : Infinity;

    if (elapsed >= Config.AUTO_REFRESH_MS) {
      // Overdue — refresh immediately (this also restarts the timer chain)
      console.info('Clock: recovering after ' + Math.round(elapsed / 1000) + 's. Refreshing now.');
      requestUpdate();
    } else {
      // Not yet due, but the timer may have silently died.
      // Cancel whatever might be pending and reschedule for the remaining time.
      if (state.refreshTimer) {
        clearTimeout(state.refreshTimer);
      }
      var remaining = Config.AUTO_REFRESH_MS - elapsed;
      state.refreshTimer = setTimeout(function () {
        requestUpdate();
      }, remaining);
    }
  }

  function handleVisibilityChange() {
    if (document.visibilityState === 'visible') {
      ensureTimerAlive();
    }
  }

  function handleWindowFocus() {
    ensureTimerAlive();
  }

  // Attach once at module level (safe even if init is called multiple times)
  if (typeof document.addEventListener === 'function') {
    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('focus', handleWindowFocus);
  }

  // ─── Public API ──────────────────────────────────────────────────
  return {
    init: init
  };

})(jQuery, moment, ClockConfig, ClockAstro, ClockRender);
