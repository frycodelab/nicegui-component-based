/* NiceStack service worker: offline-friendly caching for the app shell.
   Static assets use stale-while-revalidate; navigations are network-first with an
   offline fallback. NiceGUI's realtime channels and API routes are never intercepted. */

const CACHE = 'nicestack-v1';
const PRECACHE = [
  '/assets/css/global-css.css',
  '/assets/css/icons.css',
  '/assets/images/logo.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Leave NiceGUI's websocket/SSE and API traffic untouched.
  if (url.pathname.startsWith('/_nicegui') ||
      url.pathname.startsWith('/socket.io') ||
      url.pathname.startsWith('/api')) {
    return;
  }

  // Static assets: serve from cache, refresh in the background.
  if (url.pathname.startsWith('/assets/')) {
    event.respondWith(
      caches.open(CACHE).then((cache) =>
        cache.match(req, { ignoreSearch: true }).then((cached) => {
          const network = fetch(req).then((resp) => {
            if (resp && resp.status === 200) cache.put(req, resp.clone());
            return resp;
          }).catch(() => cached);
          return cached || network;
        })
      )
    );
    return;
  }

  // Page navigations: try the network first, fall back to cache, then an offline page.
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(() =>
        caches.match(req, { ignoreSearch: true }).then((cached) =>
          cached || new Response(
            '<!doctype html><meta charset="utf-8"><title>Offline</title>' +
            '<body style="font-family:sans-serif;padding:2rem;color:#18181b">' +
            'You are offline. Reconnect and try again.</body>',
            { headers: { 'Content-Type': 'text/html' } }
          )
        )
      )
    );
  }
});
