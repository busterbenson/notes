/**
 * clock13-config.js
 * Configuration constants for the Quirky Clock.
 * Edit this file to tune visual appearance without touching logic.
 */

var ClockConfig = (function () {
  'use strict';

  // ─── Clock Geometry ───────────────────────────────────────────────
  // Sunset is pinned to this angle on the dial (right side = 90°)
  var SUNSET_PIN_DEGREES = 90;

  // How many degrees = 1 hour on the 24-hour dial
  var DEGREES_PER_HOUR = 15;    // 360 / 24
  var DEGREES_PER_MINUTE = 0.25; // 15 / 60

  // ─── Concentric Circle Ranges ─────────────────────────────────────
  // The sun oscillates between these lines across the year (solstice extremes)
  var SUN_LINE_AMPLITUDE = 3; // -3 (winter) to +3 (summer)

  // Maximum line offset from the sun for each body
  // [0] = range at equinox (used as base), scaled by season
  var PLANET_LINE_RANGES = {
    moon:    { base: 6, max: 8 },
    mercury: { base: 1, max: 2 },
    venus:   { base: 2, max: 3 },
    mars:    { base: 3, max: 4 },
    jupiter: { base: 4, max: 5 },
    saturn:  { base: 5, max: 6 },
    uranus:  { base: 6, max: 7 },
    neptune: { base: 6, max: 7 },
    pluto:   { base: 7, max: 7 }
  };

  // Maximum elongation from the sun (degrees) for inner planets
  var MAX_ELONGATION = {
    mercury: 28,
    venus: 47
  };

  // ─── Planet Metadata ──────────────────────────────────────────────
  // Order determines rendering order (first = innermost / highest z-index)
  var PLANETS = [
    { name: 'Sun',     token: 'sun',     imagePath: 'v2/sun/sun',           hasLabel: false },
    { name: 'Moon',    token: 'moon',    imagePath: 'v2/moon/full/moon',    hasLabel: false },
    { name: 'Mercury', token: 'mercury', imagePath: 'v2/mercury/mercury',   hasLabel: true },
    { name: 'Venus',   token: 'venus',   imagePath: 'v2/venus/venus',       hasLabel: true },
    { name: 'Mars',    token: 'mars',    imagePath: 'v2/mars/mars',         hasLabel: true },
    { name: 'Jupiter', token: 'jupiter', imagePath: 'v2/jupiter/jupiter',   hasLabel: true },
    { name: 'Saturn',  token: 'saturn',  imagePath: 'v2/saturn/saturn',     hasLabel: true },
    { name: 'Uranus',  token: 'uranus',  imagePath: 'v2/uranus/uranus',     hasLabel: true },
    { name: 'Neptune', token: 'neptune', imagePath: 'v2/neptune/neptune',   hasLabel: true },
    { name: 'Pluto',   token: 'pluto',   imagePath: 'v2/pluto/pluto',       hasLabel: true }
  ];

  // Inner planets (orbit between Earth and Sun)
  var INNER_PLANETS = ['mercury', 'venus'];

  // Outer planets (orbit beyond Earth)
  var OUTER_PLANETS = ['mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'];

  // ─── Moon Phase Image Paths ───────────────────────────────────────
  var MOON_PHASE_IMAGES = {
    'NEW_MOON':        'v2/moon/new/moon',
    'WAXING_CRESCENT': 'v2/moon/waxing_crescent/moon',
    'FIRST_QUARTER':   'v2/moon/first_quarter/moon',
    'WAXING_GIBBOUS':  'v2/moon/waxing_gibbous/moon',
    'FULL_MOON':       'v2/moon/full/moon',
    'WANING_GIBBOUS':  'v2/moon/waning_gibbous/moon',
    'LAST_QUARTER':    'v2/moon/third_quarter/moon',
    'WANING_CRESCENT': 'v2/moon/waning_crescent/moon'
  };

  // Map SunCalc phase (0-1) to the API's phase name
  // SunCalc: 0 = new, 0.25 = first quarter, 0.5 = full, 0.75 = last quarter
  function moonPhaseNameFromFraction(phase) {
    if (phase < 0.0625)  return 'NEW_MOON';
    if (phase < 0.1875)  return 'WAXING_CRESCENT';
    if (phase < 0.3125)  return 'FIRST_QUARTER';
    if (phase < 0.4375)  return 'WAXING_GIBBOUS';
    if (phase < 0.5625)  return 'FULL_MOON';
    if (phase < 0.6875)  return 'WANING_GIBBOUS';
    if (phase < 0.8125)  return 'LAST_QUARTER';
    if (phase < 0.9375)  return 'WANING_CRESCENT';
    return 'NEW_MOON'; // wraps around
  }

  // ─── Image Base Path ──────────────────────────────────────────────
  var IMAGE_BASE = '/assets/images/clock/11';

  // ─── Background Color Palette ─────────────────────────────────────
  var COLORS = {
    night:       '#0B1A4A',    // deep navy
    dawn:        '#1C3366',    // dark blue, hint of light
    preSunrise:  '#D08862',    // warm coral sunrise glow
    postSunrise: '#8AADCF',    // warm blue, cooling from sunrise glow
    sunrise:     '#90C8F0',    // clear morning blue (start of morning→noon)
    noon:        '#C2E2FF',    // lightest, brightest sky blue (peak)
    sunset:      '#8CBEEA',    // gentle afternoon blue (slightly less bright)
    preSunset:   '#DC8558',    // warm golden sunset glow
    postSunset:  '#A85540',    // deeper sunset ember
    evening:     '#1A3060'     // dark evening blue
  };

  // Degrees of twilight glow before/after sunrise and sunset
  var TWILIGHT_DEGREES = 5;

  // ─── Timing ───────────────────────────────────────────────────────
  var AUTO_REFRESH_MS = 60000; // 1 minute

  // ─── Default Location (Oakland, CA — used when geolocation fails) ─
  var DEFAULT_LOCATION = {
    lat: 37.8573003,
    lng: -122.2784977
  };

  // ─── Public API ───────────────────────────────────────────────────
  return {
    SUNSET_PIN_DEGREES: SUNSET_PIN_DEGREES,
    DEGREES_PER_HOUR: DEGREES_PER_HOUR,
    DEGREES_PER_MINUTE: DEGREES_PER_MINUTE,
    SUN_LINE_AMPLITUDE: SUN_LINE_AMPLITUDE,
    PLANET_LINE_RANGES: PLANET_LINE_RANGES,
    MAX_ELONGATION: MAX_ELONGATION,
    PLANETS: PLANETS,
    INNER_PLANETS: INNER_PLANETS,
    OUTER_PLANETS: OUTER_PLANETS,
    MOON_PHASE_IMAGES: MOON_PHASE_IMAGES,
    moonPhaseNameFromFraction: moonPhaseNameFromFraction,
    IMAGE_BASE: IMAGE_BASE,
    COLORS: COLORS,
    TWILIGHT_DEGREES: TWILIGHT_DEGREES,
    AUTO_REFRESH_MS: AUTO_REFRESH_MS,
    DEFAULT_LOCATION: DEFAULT_LOCATION
  };
})();
