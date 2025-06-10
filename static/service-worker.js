const CACHE_NAME = "yellowroam-cache-v1";
const urlsToCache = [
  "/",
  "/static/styles/main.css",
  "/static/images/yellowroam_logo.png",
  "/static/manifest.json",
  // Add more files as needed
];

// Install Service Worker & Precache Assets
self.addEventListener("install", (event) => {
  console.log("🛠 Service Worker installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("📦 Caching app shell...");
      return cache.addAll(urlsToCache);
    })
  );
});

// Activate Service Worker & Cleanup Old Caches
self.addEventListener("activate", (event) => {
  console.log("⚙️ Service Worker activating...");
  event.waitUntil(
    caches.keys().then((keyList) =>
      Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("🧹 Removing old cache:", key);
            return caches.delete(key);
          }
        })
      )
    )
  );
});

// Fetch Assets (Cache First Strategy)
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request);
    })
  );
});
