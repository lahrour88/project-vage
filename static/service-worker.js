const CACHE_NAME = "my-pwa-cache-v1";
const urlsToCache = [
  "/", 
  "/about",
  "/login",
  "/admin",
  "/add"
  // CSS
  "/static/style.css",
  "/static/home.css",
  "/static/add.css",
  "/static/about.css",

  // JS
  "/static/main.js",

  // أيقونات PWA
  "/static/icons/192.png",
  "/static/icons/512.png",

  // الصور
  "/static/images/img1.png",
  "/static/images/img3.png",
  "/static/images/logo.jpg",
  "/static/images/service2.jpg",
  "/static/images/service4.jpeg",
  "/static/images/service5.jpg",
  "/static/images/services2.jpg",
  "/static/images/sevice1.jpg",

  // manifest
  "/static/manifest.json"
];

// عند تثبيت الـ Service Worker
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// عند جلب أي ملف
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // إذا الملف موجود في الكاش نرجعه، وإلا نطلبه من النت
      return response || fetch(event.request);
    })
  );
});