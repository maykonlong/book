const SHELL_CACHE = 'metade-leitor-shell-v1';
const SHELL_FILES = [
  './index.html',
  './ler.html',
  './manifest.json',
  './assets/app-icon-180.png',
  './assets/app-icon-192.png',
  './assets/app-icon-512.png'
];

const homeURL = new URL('./index.html', self.registration.scope);
const readerURL = new URL('./ler.html', self.registration.scope);
const shellPaths = new Set([new URL('./', self.registration.scope).pathname, homeURL.pathname, readerURL.pathname]);
const assetPaths = new Set(SHELL_FILES.slice(2).map((path) => new URL(path, self.registration.scope).pathname));

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      .then((cache) => cache.addAll(SHELL_FILES))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(names.filter((name) => name.startsWith('metade-leitor-shell-') && name !== SHELL_CACHE).map((name) => caches.delete(name))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  if (request.mode === 'navigate' && shellPaths.has(url.pathname)) {
    const key = url.pathname === readerURL.pathname ? readerURL : homeURL;
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok) {
          const cache = await caches.open(SHELL_CACHE);
          await cache.put(key, response.clone());
        }
        return response;
      } catch (_) {
        return (await caches.match(key)) || Response.error();
      }
    })());
    return;
  }

  if (assetPaths.has(url.pathname)) {
    event.respondWith(caches.match(request).then((cached) => cached || fetch(request)));
  }
});
