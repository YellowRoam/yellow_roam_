const CACHE_NAME = "yellowroam-cache-v1";
const urlsToCache = [
  "/",  // Fallback root
  "/static/styles/main.css",
  "/static/manifest.json",
  "https://raw.githubusercontent.com/YellowRoam/yellow_roam_/main/static/yellow_roam_logo.png",
  // You can add your offline.html here later if needed
];

// Install Service Worker & Precache Assets
self.addEventListener("install", (event) => {
  console.log("🛠 Service Worker installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("📦 Caching app shell...");
      return cache.addAll(urlsToCache).catch((err) => {
        console.error("❌ Cache addAll failed:", err);
      });
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
      return fetch(event.request).catch((err) => {
        console.error("🚫 Fetch failed:", err);
      });
    })
  );
});
