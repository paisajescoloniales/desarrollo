#!/usr/bin/env python3
"""
Remove UniversalViewer CDN references from object pages (dead code - never initialized)
Object pages use Leaflet viewer instead
"""
import re
from pathlib import Path

# Get all object HTML files
paisajes_dir = Path('paisajes')
obj_files = sorted(paisajes_dir.glob('obj*.html'))

print(f"Found {len(obj_files)} object files")

for obj_file in obj_files:
    # Read the file
    content = obj_file.read_text()

    # Remove UV CSS link
    content = re.sub(
        r'\s*<!-- UniversalViewer IIIF Viewer -->\s*',
        '',
        content
    )

    content = re.sub(
        r'\s*<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/universalviewer@4\.0\.0/dist/uv\.css">\s*',
        '',
        content
    )

    # Remove UV JS script
    content = re.sub(
        r'\s*<script src="https://cdn\.jsdelivr\.net/npm/universalviewer@4\.0\.0/dist/umd/UV\.js"></script>\s*',
        '',
        content
    )

    # Write back
    obj_file.write_text(content)
    print(f"Updated {obj_file.name}")

print("Done!")
