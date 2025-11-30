#!/usr/bin/env python3
"""Fix Leaflet JavaScript script tags - remove bad integrity hash"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the bad Leaflet JS script tag
    new_content = re.sub(
        r'<!-- Leaflet JavaScript -->.*?<script src="https://unpkg\.com/leaflet@1\.9\.4/dist/leaflet\.js"[^>]*></script>',
        '<!-- Leaflet JavaScript -->\n  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>',
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Fixed {html_file.name}")

print(f"\n✓ Fixed {count} object pages")
