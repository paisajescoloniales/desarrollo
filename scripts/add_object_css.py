#!/usr/bin/env python3
"""Add object-pages.css to all object pages"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

css_link = '  <link rel="stylesheet" href="../assets/css/object-pages.css">\n'

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already added
    if 'object-pages.css' in content:
        continue

    # Add before </head>
    new_content = content.replace('</head>', css_link + '</head>')

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Added CSS to {html_file.name}")

print(f"\n✓ Added CSS to {count} object pages")
