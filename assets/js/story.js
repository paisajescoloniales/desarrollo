// -------------------------------------------
// Story runtime: Map / Timeline / Video switcher
// -------------------------------------------

let map;
let baseOverlay = null; // current L.imageOverlay for CRS.Simple
let tileLayer = null; // current L.tileLayer if using tiles
let ytPlayer;

// --- Defaults for initial map (used until a step overrides them) ---
const DEFAULT_IMAGE_SRC = "/assets/img/mapa.png";
const DEFAULT_IMAGE_W = 2048;
const DEFAULT_IMAGE_H = 1364;

// Utility: build Leaflet CRS.Simple bounds from image size
function imageBounds(w, h) {
  return [
    [0, 0],
    [h, w],
  ];
}

// Replace the static image overlay (CRS.Simple)
function replaceImageOverlay(src, w, h) {
  const bounds = imageBounds(w, h);

  // Remove tile layer if present
  if (tileLayer) {
    map.removeLayer(tileLayer);
    tileLayer = null;
  }
  // Remove old overlay
  if (baseOverlay) {
    map.removeLayer(baseOverlay);
    baseOverlay = null;
  }

  baseOverlay = L.imageOverlay(src, bounds).addTo(map);
  map.setMaxBounds(bounds);
  // Fit once when swapping background (camera will still pan/fly afterwards)
  map.fitBounds(bounds);
}

// Replace with a tile layer (e.g., OSM). Leaves CRS as default (not Simple).
function replaceTileLayer(urlTemplate, attribution = "") {
  // Remove image overlay if present
  if (baseOverlay) {
    map.removeLayer(baseOverlay);
    baseOverlay = null;
  }
  if (tileLayer) {
    map.removeLayer(tileLayer);
  }
  // If you want geographic tiles, you'd typically also re-init the map
  // without CRS.Simple. Here we keep CRS.Simple flow; only use this if
  // your coordinates/logic match.
  tileLayer = L.tileLayer(urlTemplate, { attribution }).addTo(map);
}

// Switch the visible right-side slide
function showSlide(kind) {
  const mapSlide = document.getElementById("map-slide");
  const timelineSlide = document.getElementById("timeline-slide");
  const videoSlide = document.getElementById("video-slide");

  mapSlide.classList.add("d-none");
  timelineSlide.classList.add("d-none");
  videoSlide.classList.add("d-none");

  if (kind === "timeline") timelineSlide.classList.remove("d-none");
  else if (kind === "video") videoSlide.classList.remove("d-none");
  else mapSlide.classList.remove("d-none");
}

// ---------- YouTube helpers (safe global) ----------
function extractYouTubeId(url) {
  const m =
    url.match(/youtu\.be\/([A-Za-z0-9_-]{6,})/) ||
    url.match(/[?&]v=([A-Za-z0-9_-]{6,})/) ||
    url.match(/youtube\.com\/embed\/([A-Za-z0-9_-]{6,})/);
  return m ? m[1] : null;
}

// singleton player on window (avoid redeclare errors)
window.ytPlayer = window.ytPlayer || null;

function ensureYTPlayer(videoId, start) {
  const opts = {
    videoId,
    host: "https://www.youtube.com", // or "https://www.youtube-nocookie.com"
    playerVars: {
      start: start || 0,
      rel: 0,
      mute: 1,
      playsinline: 1,
      origin: window.location.origin, // scheme+host(+port), no path
    },
  };

  if (window.ytPlayer && window.ytPlayer.loadVideoById) {
    window.ytPlayer.loadVideoById({
      videoId,
      startSeconds: opts.playerVars.start,
    });
  } else {
    window.ytPlayer = new YT.Player("yt-player", opts);
  }
}

function loadOrCueVideo(src, start = 0) {
  const id = extractYouTubeId(src);
  if (!id) return;
  if (window.YT && window.YT.Player) {
    ensureYTPlayer(id, start);
  } else {
    // API not ready yet — set callback once
    window.onYouTubeIframeAPIReady = function () {
      ensureYTPlayer(id, start);
    };
  }
}

function pauseVideo() {
  if (window.ytPlayer && window.ytPlayer.pauseVideo)
    window.ytPlayer.pauseVideo();
}

// -------------------------------------------
// Init
// -------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
  const scrollEl = document.getElementById("scroll-column");
  bootstrap.ScrollSpy.getOrCreateInstance(scrollEl, {
    target: "#story-scrollspy",
    offset: 100,
  });

  // Leaflet map with CRS.Simple for static images
  map = L.map("map", {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 2,
    zoomControl: true,
  });

  replaceImageOverlay(DEFAULT_IMAGE_SRC, DEFAULT_IMAGE_W, DEFAULT_IMAGE_H);

  setupScrollama();
});

// -------------------------------------------
// Scrollama: react to each step
// -------------------------------------------
function setupScrollama() {
  const scroller = scrollama();

  scroller
    .setup({
      step: ".step",
      offset: 0.6,
      debug: false,
    })
    .onStepEnter((response) => {
      // Visual active state
      document
        .querySelectorAll(".step")
        .forEach((el) => el.classList.remove("is-active"));
      const el = response.element;
      el.classList.add("is-active");

      // Data from the step element
      const view = el.dataset.step; // "map" | "timeline" | "video"
      const stepAnchor = el.id; // e.g., "step1" (used by scrollspy)

      // Right-panel media overrides
      const mediaType = el.dataset.mediaType; // "map-image" | "map-tile" | "video"
      const mediaSrc = el.dataset.mediaSrc || "";
      const mediaW = parseInt(el.dataset.mediaWidth || 0, 10);
      const mediaH = parseInt(el.dataset.mediaHeight || 0, 10);
      const mediaStart = parseInt(el.dataset.mediaStart || 0, 10);

      // Camera for CRS.Simple image
      const x = parseFloat(el.dataset.x);
      const y = parseFloat(el.dataset.y);
      const zoom = parseFloat(el.dataset.zoom);

      // --- Switch right column ---
      showSlide(view);

      if (view === "map") {
        // Apply per-step background override if present
        if (mediaType === "map-image" && mediaSrc && mediaW && mediaH) {
          replaceImageOverlay(mediaSrc, mediaW, mediaH);
        } else if (mediaType === "map-tile" && mediaSrc) {
          replaceTileLayer(mediaSrc, el.dataset.attribution || "");
        }
        // Fly/pan camera if numbers are valid
        if (!isNaN(x) && !isNaN(y) && !isNaN(zoom)) {
          const current = map.getZoom();
          if (zoom === current) {
            map.panTo([y, x], { animate: true, duration: 1.2 });
          } else {
            map.flyTo([y, x], zoom, { animate: true, duration: 1.5 });
          }
        }
        // Pause video if leaving video view
        pauseVideo();
      } else if (view === "video") {
        // Load/cue the requested video
        if (mediaType === "video" && mediaSrc) {
          loadOrCueVideo(mediaSrc, isNaN(mediaStart) ? 0 : mediaStart);
        }
      } else if (view === "timeline") {
        // Nothing special; iframe is static
        pauseVideo();
      }

      // --- Highlight ScrollSpy dot manually (keeps it crisp) ---
      document
        .querySelectorAll("#story-scrollspy .nav-link")
        .forEach((link) => {
          link.classList.toggle(
            "active",
            link.getAttribute("href") === `#${stepAnchor}`
          );
        });
      if (window.stepPins) {
        window.stepPins.forEach((m) => map.removeLayer(m));
      }
      window.stepPins = [];

      // Build pins for this step
      for (let i = 1; i <= 4; i++) {
        const raw = el.dataset[`pin${i}`];
        if (!raw) continue;

        const parts = raw.split("|");
        const x = parseFloat(parts[0]);
        const y = parseFloat(parts[1]);
        const label = parts[2] || "";

        if (isNaN(x) || isNaN(y)) continue;

        const marker = L.circleMarker([y, x], {
          radius: 8,
          color: "red",
          fillOpacity: 0.7,
        }).addTo(map);

        if (label) marker.bindPopup(label);
        window.stepPins.push(marker);
      }
    });
}

window.openStackedPanel = function (id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.add("is-open");
  el.setAttribute("aria-hidden", "false");
};
window.closeStackedPanel = function (id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove("is-open");
  el.setAttribute("aria-hidden", "true");
};
