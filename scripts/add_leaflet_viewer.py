#!/usr/bin/env python3
"""Replace OpenSeadragon with Leaflet image viewer in object pages"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

# Leaflet viewer template
leaflet_viewer = """      <div id="image-viewer" style="width: 100%; height: 600px; background: #000;"></div>

<script>
  document.addEventListener('DOMContentLoaded', function() {{
    var objId = '{obj_id}';
    var imageUrl = '../img/derivatives/iiif/images/' + objId + '/full/full/0/default.jpg';

    // Get image dimensions (these will be set per object)
    var img = new Image();
    img.onload = function() {{
      var bounds = [[0, 0], [img.height, img.width]];

      var map = L.map('image-viewer', {{
        crs: L.CRS.Simple,
        minZoom: -2,
        maxZoom: 2,
        zoomControl: true,
        attributionControl: false
      }});

      L.imageOverlay(imageUrl, bounds).addTo(map);
      map.fitBounds(bounds);
    }};
    img.src = imageUrl;
  }});
</script>
"""

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract object ID from filename
    obj_id = html_file.stem  # e.g., 'obj10'

    # Find and replace the entire item-view content
    # Match from prevlink through to nextlink (or end of item-view)
    pattern = re.compile(
        r"(<span class='pagination-link' id='prevlink'></span>)\s*.*?\s*(<span class='pagination-link' id='nextlink'></span>)",
        re.DOTALL
    )

    replacement = leaflet_viewer.format(obj_id=obj_id)
    new_content = pattern.sub(
        r"\1\n" + replacement + "\n    \\2",
        content
    )

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated {html_file.name}")

print(f"\n✓ Updated {count} object pages with Leaflet viewer")
