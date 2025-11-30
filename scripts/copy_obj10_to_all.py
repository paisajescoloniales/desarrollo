#!/usr/bin/env python3
"""Copy obj10 HTML to all objects, preserving only their metadata"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")

# Read obj10 as template
with open(paisajes_dir / "obj10.html", 'r', encoding='utf-8') as f:
    template = f.read()

count = 0
for html_file in sorted(paisajes_dir.glob("obj*.html")):
    if html_file.name == "obj10.html":
        continue

    # Read current file to extract metadata
    with open(html_file, 'r', encoding='utf-8') as f:
        current = f.read()

    # Extract object ID
    obj_id = html_file.stem
    obj_num = int(obj_id.replace('obj', ''))

    # Extract title from current file
    title_match = re.search(r'<title>\s*Paisajes Coloniales \| (.*?)\s*</title>', current, re.DOTALL)
    title = title_match.group(1) if title_match else "Unknown"

    # Extract h3 item-label from current file
    h3_match = re.search(r"<h3[^>]*class='item-label'[^>]*>(.*?)</h3>", current, re.DOTALL)
    h3_content = h3_match.group(1) if h3_match else title

    # Extract metadata block from current file
    metadata_match = re.search(r"(<dl class='metadata-block'>.*?</dl>)", current, re.DOTALL)
    metadata = metadata_match.group(1) if metadata_match else "<dl class='metadata-block'></dl>"

    # Calculate prev/next
    prev_obj = f"obj{obj_num - 1}.html" if obj_num > 2 else ""
    next_obj = f"obj{obj_num + 1}.html" if obj_num < 53 else ""

    # Create new HTML from template
    new_html = template

    # Replace object ID
    new_html = new_html.replace('obj10', obj_id)
    new_html = new_html.replace('obj9.html', prev_obj)
    new_html = new_html.replace('obj11.html', next_obj)

    # Replace title
    new_html = re.sub(
        r'<title>\s*Paisajes Coloniales \|.*?</title>',
        f'<title>\n    Paisajes Coloniales | {title}\n  </title>',
        new_html,
        flags=re.DOTALL
    )

    # Replace h3 item-label
    new_html = re.sub(
        r"<h3[^>]*class='item-label'[^>]*>.*?</h3>",
        f"<h3 alt=\"{h3_content.strip()}\" class='item-label'>{h3_content}</h3>",
        new_html,
        flags=re.DOTALL
    )

    # Replace metadata block
    new_html = re.sub(
        r"<dl class='metadata-block'>.*?</dl>",
        metadata,
        new_html,
        flags=re.DOTALL
    )

    # Write new file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

    count += 1
    print(f"Updated {html_file.name}")

print(f"\n✓ Updated {count} object pages")
