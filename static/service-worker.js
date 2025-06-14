const CACHE_NAME = "yellowroam-cache-v1";
const urlsToCache = [
  "/",
  "/static/styles/main.css",
  "/static/manifest.json",
  "/static/images/yellowroam_logo.png"
];

self.addEventListener("install", (event) => {
  console.log("🛠 Service Worker installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache).catch(err => {
        console.error("❌ Cache addAll failed:", err);
      });
    })
  );
});

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

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request).catch((err) => {
        console.error("❌ Fetch failed:", err);
      });
    })
  );
});
