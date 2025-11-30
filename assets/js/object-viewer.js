// Initialize Leaflet image viewer for object pages
function initObjectViewer(objId) {
  var imageUrl = '../img/derivatives/iiif/images/' + objId + '/full/full/0/default.jpg';

  var img = new Image();
  img.onload = function() {
    var bounds = [[0, 0], [img.height, img.width]];

    var map = L.map('image-viewer', {
      crs: L.CRS.Simple,
      minZoom: -2,
      maxZoom: 2,
      zoomControl: true,
      attributionControl: false
    });

    L.imageOverlay(imageUrl, bounds).addTo(map);
    map.fitBounds(bounds);
  };
  img.src = imageUrl;
}

// Auto-initialize if objId in data attribute
document.addEventListener('DOMContentLoaded', function() {
  var viewer = document.getElementById('image-viewer');
  if (viewer && viewer.dataset.objId) {
    initObjectViewer(viewer.dataset.objId);
  }
});
