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
    return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m;
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
        // Normalize the API response into a clean array
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
    sunPlot.line = Math.round(Config.SUN_LINE_AMPLITUDE * seasonalFactor);

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

      var line = computePlanetLine(token, degreesFromSun, planet.isRetrograde,
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

  // ─── Helper: compute concentric circle line for a body ───────────
  function computePlanetLine(token, degreesFromSun, isRetrograde, seasonalFactor, sunLine, moonData) {
    var ranges = Config.PLANET_LINE_RANGES[token];
    if (!ranges) return sunLine; // unknown body → same as sun

    // Scale the range by season (larger spread at solstices)
    var absSeasonFactor = Math.abs(seasonalFactor);
    var range = ranges.base + (ranges.max - ranges.base) * absSeasonFactor;

    // ── Moon: line based on illumination and waxing/waning ──────────
    if (token === 'moon') {
      if (!moonData) return sunLine;
      var illumination = moonData.illuminationPct / 100; // 0-1
      var isWaxing = moonData.isWaxing;

      // Full moon → max offset in one direction, new moon → near sun
      // Waxing: offset goes positive (above sun). Waning: offset goes negative.
      var offset;
      if (illumination > 0.5) {
        // Gibbous (half to full): offset scales from range/2 to range
        offset = range * (0.5 + illumination / 2);
      } else {
        // Crescent (new to half): offset scales from 0 to range/2
        offset = range * illumination;
      }
      // Waxing = positive offset, waning = negative
      return sunLine + Math.round(isWaxing ? offset : -offset);
    }

    // ── Inner planets: elongation-based ─────────────────────────────
    if (Config.INNER_PLANETS.indexOf(token) >= 0) {
      var maxElong = Config.MAX_ELONGATION[token];
      // How far is the planet from the sun? (0-360, but inner planets stay within maxElong)
      var elongation;
      if (degreesFromSun <= 180) {
        elongation = Math.min(degreesFromSun, maxElong);
      } else {
        elongation = Math.min(360 - degreesFromSun, maxElong);
      }
      var fraction = elongation / maxElong; // 0-1
      var sign = isRetrograde ? 1 : -1;
      return sunLine + Math.round(sign * range * fraction);
    }

    // ── Outer planets: opposition-based ─────────────────────────────
    // Max offset at opposition (180° from sun), zero at conjunction (0°)
    var opposition;
    if (degreesFromSun <= 180) {
      opposition = degreesFromSun / 180; // 0 → 1
    } else {
      opposition = (360 - degreesFromSun) / 180; // 1 → 0
    }
    var outerSign = isRetrograde ? 1 : -1;
    return sunLine + Math.round(outerSign * range * opposition);
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
    computePlotPositions: computePlotPositions
  };

})(SunCalc, moment, ClockConfig);
