/**
 * clock13-astro.js
 * Astronomical calculations for the Quirky Clock.
 * No DOM access — pure data in, data out.
 *
 * Dependencies: SunCalc (global), moment (global), ClockConfig
 */

var ClockAstro = (function (SunCalc, moment, Config) {
  'use strict';

  // ─── Utility: modulo that always returns positive ─────────────────
  function posMod(n, m) {
    return ((n % m) + m) % m;
  }

  // ─── Utility: day of year (1-366) ────────────────────────────────
  function dayOfYear(date) {
    var start = new Date(date.getFullYear(), 0, 0);
    var diff = date - start;
    var oneDay = 86400000; // ms per day
    return Math.floor(diff / oneDay);
  }

  // ─── Utility: convert hours + minutes to clock degrees ───────────
  // On the 24-hour dial: 0h = 0°, 6h = 90°, 12h = 180°, 18h = 270°
  function timeToDegrees(hours, minutes, seconds) {
    seconds = seconds || 0;
    return posMod(
      hours * Config.DEGREES_PER_HOUR +
      minutes * Config.DEGREES_PER_MINUTE +
      seconds * (Config.DEGREES_PER_MINUTE / 60),
      360
    );
  }

  // ─── Utility: degrees back to HH:MM string ──────────────────────
  function degreesToTimeString(degrees) {
    degrees = posMod(degrees, 360);
    var totalMinutes = degrees / Config.DEGREES_PER_MINUTE;
    var h = Math.floor(totalMinutes / 60);
    var m = Math.floor(totalMinutes % 60);
    return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m;
  }

  // ─── Utility: extract HH, MM, SS from a Date ────────────────────
  function dateToTimeDegrees(date) {
    return timeToDegrees(date.getHours(), date.getMinutes(), date.getSeconds());
  }

  // ─── 1. Seasonal Data (via SunCalc) ──────────────────────────────
  /**
   * Returns sunrise/sunset/moon data for a given date and location.
   * All times are in the user's local timezone (via JS Date).
   */
  function getSeasonalData(lat, lng, date) {
    var times = SunCalc.getTimes(date, lat, lng);
    var moonIllum = SunCalc.getMoonIllumination(date);
    var moonTimes = SunCalc.getMoonTimes(date, lat, lng);
    var moonPos = SunCalc.getMoonPosition(date, lat, lng);

    // SunCalc may return NaN for sunrise/sunset at extreme latitudes
    var sunrise = isNaN(times.sunrise) ? null : times.sunrise;
    var sunset  = isNaN(times.sunset)  ? null : times.sunset;
    var solarNoon = isNaN(times.solarNoon) ? null : times.solarNoon;

    var sunriseDeg = sunrise ? dateToTimeDegrees(sunrise) : null;
    var sunsetDeg  = sunset  ? dateToTimeDegrees(sunset)  : null;
    var solarNoonDeg = solarNoon ? dateToTimeDegrees(solarNoon) : null;

    // Moon phase from SunCalc: 0 = new, 0.25 = first quarter, 0.5 = full, 0.75 = last quarter
    var moonPhaseFraction = moonIllum.phase;         // 0-1 continuous
    var moonIlluminationPct = Math.round(moonIllum.fraction * 100); // 0-100%
    var isWaxing = moonPhaseFraction < 0.5;
    var phaseName = Config.moonPhaseNameFromFraction(moonPhaseFraction);

    return {
      date: moment(date).format('YYYY-MM-DD'),
      sunrise: sunrise,
      sunset: sunset,
      solarNoon: solarNoon,
      sunriseDeg: sunriseDeg,
      sunsetDeg: sunsetDeg,
      solarNoonDeg: solarNoonDeg,
      sunriseTimeStr: sunrise ? formatTime(sunrise) : '--:--',
      sunsetTimeStr:  sunset  ? formatTime(sunset)  : '--:--',
      solarNoonTimeStr: solarNoon ? formatTime(solarNoon) : '--:--',
      dayLengthHours: (sunrise && sunset) ? (sunset - sunrise) / 3600000 : null,
      moon: {
        illuminationPct: moonIlluminationPct,
        phaseFraction: moonPhaseFraction,
        phaseName: phaseName,
        isWaxing: isWaxing,
        altitude: moonPos.altitude * (180 / Math.PI),  // radians to degrees
        azimuth: moonPos.azimuth * (180 / Math.PI),
        distance: moonPos.distance,
        parallacticAngle: moonPos.parallacticAngle * (180 / Math.PI),
        moonrise: moonTimes.rise || null,
        moonset: moonTimes.set || null,
        moonriseDeg: moonTimes.rise ? dateToTimeDegrees(moonTimes.rise) : null,
        moonsetDeg:  moonTimes.set  ? dateToTimeDegrees(moonTimes.set)  : null
      }
    };
  }

  function formatTime(date) {
    var h = date.getHours();
    var m = date.getMinutes();
    var ampm = h >= 12 ? 'pm' : 'am';
    var h12 = h % 12 || 12;
    return h12 + ':' + (m < 10 ? '0' : '') + m + ' ' + ampm;
  }

  // ─── 2. Planetary Positions (via Astrology API) ──────────────────
  /**
   * Fetches ecliptic longitudes for all planets from astrologyapi.com.
   * Returns a promise resolving to an array of planet objects.
   */
  function getPlanetaryPositions(date, currentTimeDeg, lat, lng, tzOffset, apiUserId, apiKey) {
    var dateStr = moment(date).format('YYYY-MM-DD');
    var dateBits = dateStr.split('-');
    var timeStr = degreesToTimeString(currentTimeDeg);
    var timeBits = timeStr.split(':');
    var auth = 'Basic ' + btoa(apiUserId + ':' + apiKey);

    var params = {
      day: parseInt(dateBits[2], 10),
      month: parseInt(dateBits[1], 10),
      year: parseInt(dateBits[0], 10),
      hour: parseInt(timeBits[0], 10),
      min: parseInt(timeBits[1], 10),
      lat: lat,
      lon: lng,
      tzone: tzOffset,
      house_type: 'whole_sign'
    };

    return $.ajax({
      url: 'https://json.astrologyapi.com/v1/planets/tropical',
      method: 'POST',
      dataType: 'json',
      timeout: 15000, // 15 second timeout
      headers: {
        'authorization': auth,
        'Content-Type': 'application/json'
      },
      data: JSON.stringify(params)
    }).then(
      function (resp) {
        // Normalize the API response into a clean array, filtering to known bodies only
        // (API may return Ascendant, Midheaven, Rahu, Ketu etc. which we don't render)
        return resp.map(function (p) {
          return {
            name: p.name,
            token: p.name.toLowerCase(),
            eclipticLongitude: p.fullDegree,    // degrees from Aries 0, counter-clockwise
            normDegree: p.normDegree,
            sign: p.sign,
            isRetrograde: p.isRetro === 'true' || p.isRetro === true,
            speed: p.speed,
            house: p.house
          };
        }).filter(function (p) {
          return Config.KNOWN_TOKENS.indexOf(p.token) >= 0;
        });
      },
      function (err) {
        console.error('Astrology API error:', err);
        return [];
      }
    );
  }

  // ─── 3. Compute Plot Positions ───────────────────────────────────
  /**
   * Given seasonal data, planet positions, and current time,
   * compute where everything goes on the clock dial.
   *
   * Returns { plots, moments, plotOffset, constellations }
   */
  function computePlotPositions(seasonalData, planets, currentTimeDeg) {
    var sunsetDeg = seasonalData.sunsetDeg;
    var sunriseDeg = seasonalData.sunriseDeg;
    var solarNoonDeg = seasonalData.solarNoonDeg;

    // If we don't have sunrise/sunset (polar regions), use defaults
    if (sunsetDeg === null) sunsetDeg = 270; // 18:00
    if (sunriseDeg === null) sunriseDeg = 90; // 06:00
    if (solarNoonDeg === null) solarNoonDeg = 180; // 12:00

    // ── Step A: Map current time to clock, pinning sunset at 90° ────
    var plotOffset = posMod(
      Config.SUNSET_PIN_DEGREES + currentTimeDeg - sunsetDeg,
      360
    );

    // ── Step B: Compute sunrise/sunset positions on the clock ───────
    var sunriseMoment = computeMomentDegrees(sunriseDeg, sunsetDeg);
    var sunsetMoment  = computeMomentDegrees(sunsetDeg, sunsetDeg);
    var solarNoonMoment = computeMomentDegrees(solarNoonDeg, sunsetDeg);

    // Balance sunrise and sunset symmetrically around the vertical axis
    var sunriseSunsetOffset = (Config.SUNSET_PIN_DEGREES - (360 - sunriseMoment)) / 2;
    sunriseMoment -= sunriseSunsetOffset;
    sunsetMoment  -= sunriseSunsetOffset;
    solarNoonMoment -= sunriseSunsetOffset;
    plotOffset -= sunriseSunsetOffset;

    var moments = {
      sunrise:   { degrees: sunriseMoment },
      sunset:    { degrees: sunsetMoment },
      solarNoon: { degrees: solarNoonMoment }
    };

    // ── Step C: Sun position ────────────────────────────────────────
    var sun = findPlanet(planets, 'Sun');
    if (!sun) {
      // Estimate sun position from day-of-year if API didn't return it
      var estimatedDoy = dayOfYear(new Date(seasonalData.date));
      sun = { name: 'Sun', token: 'sun', eclipticLongitude: posMod((estimatedDoy - 80) * (360 / 365.25), 360), isRetrograde: false };
    }
    var sunPlot = {
      name: 'Sun',
      token: 'sun',
      eclipticLongitude: sun ? sun.eclipticLongitude : 0,
      relativeToSunDeg: 0,
      degrees: posMod(plotOffset, 360),
      isAboveHorizon: false,
      isVisible: false,
      isRetrograde: false,
      line: 0
    };
    sunPlot.isAboveHorizon = isAboveHorizon(sunPlot.degrees);

    // ── Step D: Compute sun's concentric line (seasonal) ────────────
    var doy = dayOfYear(new Date(seasonalData.date));
    // Sine wave: peaks at summer solstice (~day 172), troughs at winter solstice
    // Phase offset 80 aligns the zero-crossings with the equinoxes (~day 80 = Mar 21)
    var seasonalFactor = Math.sin(2 * Math.PI * (doy - 80) / 365.25);
    sunPlot.line = Math.max(Config.LINE_MIN, Math.min(Config.LINE_MAX,
      Math.round(Config.SUN_LINE_AMPLITUDE * seasonalFactor)));

    // ── Step E: Constellations ──────────────────────────────────────
    // The constellation ring image has the zodiac running counter-clockwise
    // (natural sky view). To align it so that the sun's current zodiac sign
    // appears behind the sun's hand on the clock, we rotate by:
    //   sunPlot.degrees + sun.eclipticLongitude
    // This ensures ecliptic longitude L maps to the correct clock angle
    // for all bodies simultaneously.
    var ariesRelative = sun ? posMod(360 - sun.eclipticLongitude, 360) : 0;
    var constellations = {
      name: 'Constellations',
      token: 'constellations',
      degrees: posMod(sunPlot.degrees + sun.eclipticLongitude, 360)
    };

    // ── Step F: Plot each planet ────────────────────────────────────
    var plots = { sun: sunPlot };
    var handOrder = ['moon', 'sun']; // moon rendered first (innermost after sun)

    for (var i = 1; i < planets.length; i++) {
      var planet = planets[i];
      var token = planet.token;

      // Degrees relative to sun on the ecliptic
      var degreesFromSun = posMod(planet.eclipticLongitude - sun.eclipticLongitude, 360);

      // Clock angle: sun's ecliptic offset minus planet's, plus the time offset
      var planetClockDeg = posMod(
        (sun.eclipticLongitude - planet.eclipticLongitude) + plotOffset,
        360
      );

      var aboveHorizon = isAboveHorizon(planetClockDeg);
      var visible = false;
      if (aboveHorizon && !sunPlot.isAboveHorizon) {
        // Planet is up and sun is down → potentially visible
        // Give 10° buffer from horizon for visibility
        if (planetClockDeg > 280 || planetClockDeg < 80) {
          visible = true;
        }
      }

      var line = computePlanetLine(token, planet.eclipticLongitude,
                                    new Date(seasonalData.date),
                                    seasonalFactor, sunPlot.line, seasonalData.moon);

      plots[token] = {
        name: planet.name,
        token: token,
        eclipticLongitude: planet.eclipticLongitude,
        relativeToSunDeg: degreesFromSun,
        degrees: planetClockDeg,
        isAboveHorizon: aboveHorizon,
        isVisible: visible,
        isRetrograde: planet.isRetrograde,
        sign: planet.sign,
        line: line
      };

      // Determine rendering order: retrograde inner planets go inside the sun
      if (token === 'moon') {
        // moon already in handOrder
      } else if (Config.INNER_PLANETS.indexOf(token) >= 0 && planet.isRetrograde) {
        handOrder.splice(1, 0, token); // insert before sun
      } else {
        handOrder.push(token);
      }
    }

    return {
      plots: plots,
      moments: moments,
      plotOffset: plotOffset,
      constellations: constellations,
      handOrder: handOrder,
      seasonalFactor: seasonalFactor,
      ariesRelative: ariesRelative
    };
  }

  // ─── Helper: compute a moment's clock position ───────────────────
  function computeMomentDegrees(momentDeg, sunsetDeg) {
    // Compute midnight offset so that sunset maps to 90°
    var midnightDeg = posMod(Config.SUNSET_PIN_DEGREES - sunsetDeg, 360);
    return posMod(midnightDeg + momentDeg, 360);
  }

  // ─── Helper: is a clock angle above the horizon? ─────────────────
  // Top of the clock (0° / 360°) = above. Left/right (90°/270°) = horizon.
  function isAboveHorizon(degrees) {
    return degrees > 270 || degrees < 90;
  }

  // ─── Helper: find a planet by name in the API array ──────────────
  function findPlanet(planets, name) {
    for (var i = 0; i < planets.length; i++) {
      if (planets[i].name === name) return planets[i];
    }
    return null;
  }

  // ─── Helper: clamp a line value to valid image range ─────────────
  function clampLine(line) {
    return Math.max(Config.LINE_MIN, Math.min(Config.LINE_MAX, line));
  }

  // ─── Ecliptic Latitude Computation ─────────────────────────────
  //
  // Each planet orbits in a plane tilted relative to the ecliptic.
  // The ecliptic latitude β (how far above/below the ecliptic plane)
  // is computed from:
  //
  //   β = arcsin( sin(i) × sin(L - Ω) )
  //
  // where:
  //   i = orbital inclination to the ecliptic
  //   L = planet's current ecliptic longitude
  //   Ω = longitude of ascending node (where the orbit crosses the ecliptic going north)
  //
  // All values from J2000.0 epoch with slow secular drift rates.
  // Sources: Meeus "Astronomical Algorithms", JPL planetary fact sheets.
  //
  // Note: For the Moon, inclination is to the ecliptic (~5.145°) and the
  // node regresses with an 18.6-year period.

  var ORBITAL_ELEMENTS = {
    //              inclination (°)   node at J2000 (°)   node drift (°/century)
    moon:    { i:  5.145,   node0: 125.044,  nodeDrift: -1934.136 }, // 18.6-yr regression
    mercury: { i:  7.005,   node0:  48.331,  nodeDrift:   -0.125 },
    venus:   { i:  3.395,   node0:  76.680,  nodeDrift:   -0.278 },
    mars:    { i:  1.850,   node0:  49.558,  nodeDrift:   -0.293 },
    jupiter: { i:  1.303,   node0: 100.464,  nodeDrift:    0.176 },
    saturn:  { i:  2.489,   node0: 113.666,  nodeDrift:   -0.252 },
    uranus:  { i:  0.773,   node0:  74.006,  nodeDrift:    0.074 },
    neptune: { i:  1.770,   node0: 131.784,  nodeDrift:   -0.006 },
    pluto:   { i: 17.160,   node0: 110.307,  nodeDrift:   -0.009 }
  };

  /**
   * Compute ecliptic latitude for a body given its ecliptic longitude and date.
   * Returns degrees, positive = north of ecliptic, negative = south.
   */
  function computeEclipticLatitude(token, eclipticLongitude, date) {
    var elem = ORBITAL_ELEMENTS[token];
    if (!elem) return 0; // Sun is always on the ecliptic (β = 0)

    // Centuries since J2000.0
    var j2000 = new Date(Date.UTC(2000, 0, 1, 12, 0, 0));
    var T = (date.getTime() - j2000.getTime()) / (86400000 * 36525);

    // Current longitude of ascending node
    var node = posMod(elem.node0 + elem.nodeDrift * T, 360);

    // β = arcsin( sin(i) × sin(L - Ω) )
    var iRad = elem.i * Math.PI / 180;
    var argRad = (eclipticLongitude - node) * Math.PI / 180;
    var beta = Math.asin(Math.sin(iRad) * Math.sin(argRad));

    return beta * 180 / Math.PI; // convert back to degrees
  }

  // ─── Helper: compute concentric circle line for a body ───────────
  //
  // Now based on ACTUAL ecliptic latitude: how far above or below
  // the ecliptic plane the body appears. Positive latitude (north of
  // ecliptic) → positive line offset, negative → negative offset.
  //
  // The line value is computed as:
  //   sunLine + round( (β / maxβ) × range )
  //
  // where maxβ is the body's maximum possible ecliptic latitude
  // (= its orbital inclination), giving a -1 to +1 normalized factor
  // that scales the configured range.

  function computePlanetLine(token, eclipticLongitude, date, seasonalFactor, sunLine, moonData) {
    var elem = ORBITAL_ELEMENTS[token];
    if (!elem) return sunLine; // unknown body → same as sun

    var ranges = Config.PLANET_LINE_RANGES[token];
    if (!ranges) return sunLine;

    // Scale the range by season (larger spread at solstices)
    var absSeasonFactor = Math.abs(seasonalFactor);
    var range = ranges.base + (ranges.max - ranges.base) * absSeasonFactor;

    // Compute actual ecliptic latitude
    var beta = computeEclipticLatitude(token, eclipticLongitude, date);

    // Normalize: β ranges from -inclination to +inclination
    // Map to -1..+1 factor
    var maxBeta = elem.i; // maximum possible latitude = orbital inclination
    var factor = beta / maxBeta; // -1 to +1

    return clampLine(sunLine + Math.round(factor * range));
  }

  // ─── 4. Local Planet Position Estimator (fallback) ───────────────
  /**
   * Estimates ecliptic longitudes for all planets using mean orbital elements.
   * Uses J2000.0 epoch (2000-01-01 12:00 TT) as reference and mean daily motion.
   * Accuracy: ~1-5° for inner planets, ~1-2° for outer planets over a few years.
   * Good enough for clock arm sizing when the API is unavailable.
   */
  function estimatePlanetaryPositions(date) {
    // Days since J2000.0 epoch (2000-01-01 12:00 UTC)
    var j2000 = new Date(Date.UTC(2000, 0, 1, 12, 0, 0));
    var daysSinceJ2000 = (date.getTime() - j2000.getTime()) / 86400000;

    // Mean orbital elements at J2000.0: longitude at epoch + mean daily motion
    // Sources: Meeus "Astronomical Algorithms", JPL approximate positions
    var bodies = [
      { name: 'Sun',     token: 'sun',     L0: 280.460,  rate: 0.9856474 },  // Earth's orbital motion as seen from Earth
      { name: 'Moon',    token: 'moon',    L0: 218.316,  rate: 13.176396 },  // Moon's mean longitude
      { name: 'Mercury', token: 'mercury', L0: 252.251,  rate: 4.0923344 },
      { name: 'Venus',   token: 'venus',   L0: 181.980,  rate: 1.6021302 },
      { name: 'Mars',    token: 'mars',    L0: 355.433,  rate: 0.5240208 },
      { name: 'Jupiter', token: 'jupiter', L0: 34.351,   rate: 0.0831294 },
      { name: 'Saturn',  token: 'saturn',  L0: 50.077,   rate: 0.0334442 },
      { name: 'Uranus',  token: 'uranus',  L0: 314.055,  rate: 0.0117260 },
      { name: 'Neptune', token: 'neptune', L0: 304.349,  rate: 0.0059540 },
      { name: 'Pluto',   token: 'pluto',   L0: 238.929,  rate: 0.0039780 }
    ];

    return bodies.map(function (b) {
      var longitude = posMod(b.L0 + b.rate * daysSinceJ2000, 360);
      return {
        name: b.name,
        token: b.token,
        eclipticLongitude: longitude,
        isRetrograde: false  // Can't easily determine from mean elements alone
      };
    });
  }

  // ─── Public API ───────────────────────────────────────────────────
  return {
    posMod: posMod,
    dayOfYear: dayOfYear,
    timeToDegrees: timeToDegrees,
    degreesToTimeString: degreesToTimeString,
    dateToTimeDegrees: dateToTimeDegrees,
    getSeasonalData: getSeasonalData,
    getPlanetaryPositions: getPlanetaryPositions,
    estimatePlanetaryPositions: estimatePlanetaryPositions,
    computeEclipticLatitude: computeEclipticLatitude,
    computePlotPositions: computePlotPositions
  };

})(SunCalc, moment, ClockConfig);
