#!/usr/bin/env python3
import re
from pathlib import Path

# Pattern to match the viewer script block
viewer_pattern = re.compile(
    r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\',.*?}\);\s*</script>',
    re.DOTALL
)

# Get all object HTML files
paisajes_dir = Path('paisajes')
obj_files = sorted(paisajes_dir.glob('obj*.html'))

print(f"Found {len(obj_files)} object files")

for obj_file in obj_files:
    # Extract object ID from filename
    obj_id = obj_file.stem  # e.g., 'obj10'

    # Read the file
    content = obj_file.read_text()

    # Add data-obj-id attribute to the div
    content = re.sub(
        r'<div id="image-viewer"',
        f'<div id="image-viewer" data-obj-id="{obj_id}"',
        content
    )

    # Replace the viewer script block with external script reference
    content = viewer_pattern.sub(
        '<script src="../assets/js/object-viewer.js"></script>',
        content
    )

    # Write back
    obj_file.write_text(content)
    print(f"Updated {obj_file.name}")

print("Done!")
