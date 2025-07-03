document.addEventListener("DOMContentLoaded", function () {
  const imageWidth = 1846;
  const imageHeight = 1500;
  const mapBounds = [
    [0, 0],
    [imageHeight, imageWidth],
  ];

  const map = L.map("map", {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 2,
    zoomSnap: 0.25,
    maxBounds: mapBounds,
    maxBoundsViscosity: 1.0,
  });

  L.imageOverlay("/assets/img/mapa0.jpg", mapBounds).addTo(map);
  map.fitBounds(mapBounds);
});
