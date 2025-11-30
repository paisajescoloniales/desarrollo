#!/usr/bin/env python3
"""Fix absolute paths in object pages to relative paths"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")
count = 0

replacements = [
    # Navigation links
    (r'href="/index\.html"', r'href="../index.html"'),
    (r'href="/historia\.html"', r'href="../historia.html"'),
    (r'href="/explora\.html"', r'href="../explora.html"'),
    (r'href="/coleccion\.html"', r'href="../coleccion.html"'),
    (r'href="/profesores\.html"', r'href="../profesores.html"'),
    (r'href="/acerca\.html"', r'href="../acerca.html"'),

    # Assets
    (r'href="/assets/', r'href="../assets/'),
    (r'src="/assets/', r'src="../assets/'),

    # Pagination links (stay within paisajes directory)
    (r"href='/paisajes/", r"href='"),
    (r'href="/paisajes/', r'href="'),
]

for html_file in sorted(paisajes_dir.glob("obj*.html")):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, new_content)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Fixed paths in {html_file.name}")

print(f"\n✓ Fixed {count} object pages")
