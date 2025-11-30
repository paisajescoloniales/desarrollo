#!/usr/bin/env python3
"""Remove OpenSeadragon script blocks from object pages"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

# Pattern to match the OpenSeadragon script block
openseadragon_pattern = re.compile(
    r'<script>\s*document\.addEventListener.*?OpenSeadragon\({.*?}\);\s*}\);\s*</script>\s*',
    re.DOTALL
)

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = openseadragon_pattern.sub('', content)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Cleaned {html_file.name}")

print(f"\n✓ Cleaned {count} object pages")
