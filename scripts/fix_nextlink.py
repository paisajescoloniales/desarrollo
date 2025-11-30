#!/usr/bin/env python3
"""Add missing nextlink span after Leaflet viewer script"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if nextlink is missing and viewer exists
    if "img.src = imageUrl;" in content:
        # Add nextlink span after the Leaflet script and before closing </div> of item-view
        # Also need to add the closing </div> if it's missing
        new_content = re.sub(
            r"(  }}\);\n</script>)\n(<dl class='metadata-block'>)",
            r"\1\n<span class='pagination-link' id='nextlink'></span>\n  </div>\n  \n\n\n\n  <script type='text/javascript'>\n    $('#prevlink').append(`<a href='' display='none'>&#8249;</a>`);\n    $('#nextlink').append(`<a href='' display='none'>&#8250;</a>`);\n  </script>\n\n\n\n\n\n\n\n\n\2",
            content
        )

        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Added nextlink to {html_file.name}")

print(f"\n✓ Fixed {count} object pages")
