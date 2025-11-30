#!/usr/bin/env python3
"""Add Leaflet JavaScript to object pages"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

# Leaflet JS script tag (without integrity - using unpkg CDN)
leaflet_js = '''
  <!-- Leaflet JavaScript -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'''

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if Leaflet JS is already included
    if 'leaflet.js' in content or 'leaflet@1.9.4/dist/leaflet.js' in content:
        continue

    # Add Leaflet JS after Leaflet CSS
    new_content = re.sub(
        r'(<!-- Leaflet CSS -->.*?</head>)',
        lambda m: m.group(1).replace('</head>', leaflet_js + '\n</head>'),
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Added Leaflet JS to {html_file.name}")

print(f"\n✓ Updated {count} object pages")
