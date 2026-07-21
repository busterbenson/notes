// Offline cache for /questions/. Bump the version to force clients to refresh
// their cached copy after the page changes.
const CACHE = 'questions-v3';
const ASSETS = [
  './',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// The page itself is network-first: an online open always shows the latest
// version, and an offline (or stalled — >3.5s) open falls back to the cached
// copy. Cache-first would show a stale page until the *next* launch, and iOS
// home-screen apps resume from the app switcher without relaunching, so that
// next launch can be days away.
const NETWORK_TIMEOUT_MS = 3500;

function networkFirst(req) {
  return new Promise((resolve) => {
    let settled = false;
    const useCache = () => caches.match(req, { ignoreSearch: true }).then((cached) => {
      if (!settled && cached) { settled = true; resolve(cached); }
      return cached;
    });
    const timer = setTimeout(useCache, NETWORK_TIMEOUT_MS);
    fetch(req).then((resp) => {
      clearTimeout(timer);
      if (resp && resp.ok) {
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
        if (!settled) { settled = true; resolve(resp); }
      } else {
        useCache().then((cached) => {
          if (!settled) { settled = true; resolve(cached || resp); }
        });
      }
    }).catch(() => {
      clearTimeout(timer);
      useCache().then((cached) => {
        if (!settled && !cached) { settled = true; resolve(Response.error()); }
      });
    });
  });
}

// Icons and manifest change rarely: cache-first with a background refresh.
function cacheFirst(req) {
  return caches.match(req, { ignoreSearch: true }).then((cached) => {
    const fetched = fetch(req).then((resp) => {
      if (resp && resp.ok) {
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
      }
      return resp;
    }).catch(() => cached);
    return cached || fetched;
  });
}

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  const isPage = e.request.mode === 'navigate' || e.request.destination === 'document';
  e.respondWith(isPage ? networkFirst(e.request) : cacheFirst(e.request));
});
