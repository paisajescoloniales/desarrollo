#!/usr/bin/env python3
"""Fix all object page viewers to match obj10's correct structure"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

# The correct viewer template (matching obj10's structure)
viewer_template = """  <div class='item-view'>
    <span class='pagination-link' id='prevlink'></span>



      <div id="image-viewer" style="width: 100%; height: 600px; background: #000;"></div>

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
<span class='pagination-link' id='nextlink'></span>
  </div>




  <script type='text/javascript'>
    $('#prevlink').append(`<a href='{prev_obj}' display='none'>&#8249;</a>`);
    $('#nextlink').append(`<a href='{next_obj}' display='none'>&#8250;</a>`);
  </script>"""

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract object ID
    obj_id = html_file.stem
    obj_num = int(obj_id.replace('obj', ''))

    # Calculate prev/next object IDs
    prev_obj = f"obj{obj_num - 1}.html" if obj_num > 2 else ""
    next_obj = f"obj{obj_num + 1}.html" if obj_num < 53 else ""

    # Replace from <div class='item-view'> to the pagination script
    pattern = re.compile(
        r"<div class='item-view'>.*?</script>\s*\n\s*\n",
        re.DOTALL
    )

    replacement = viewer_template.format(
        obj_id=obj_id,
        prev_obj=prev_obj,
        next_obj=next_obj
    ) + "\n\n\n\n\n\n\n\n"

    new_content = pattern.sub(replacement, content)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Fixed {html_file.name}")

print(f"\n✓ Fixed {count} object pages")
