#!/usr/bin/env python3
"""Apply obj10's working structure to all other object pages"""

import re
from pathlib import Path

paisajes_dir = Path("paisajes")

# Read obj10 as the template
with open(paisajes_dir / "obj10.html", 'r', encoding='utf-8') as f:
    template = f.read()

# Extract the viewer section from obj10 (from <div class='item-view'> to </script>)
viewer_pattern = re.compile(
    r"(<div class='item-view'>.*?<script type='text/javascript'>.*?</script>)",
    re.DOTALL
)
viewer_template = viewer_pattern.search(template).group(1)

count = 0
for html_file in sorted(paisajes_dir.glob("obj*.html")):
    if html_file.name == "obj10.html":
        continue  # Skip obj10 itself

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract object ID
    obj_id = html_file.stem
    obj_num = int(obj_id.replace('obj', ''))

    # Calculate prev/next
    prev_obj = f"obj{obj_num - 1}.html" if obj_num > 2 else ""
    next_obj = f"obj{obj_num + 1}.html" if obj_num < 53 else ""

    # Create viewer section for this object
    new_viewer = viewer_template.replace('obj10', obj_id)
    new_viewer = new_viewer.replace("obj9.html", prev_obj)
    new_viewer = new_viewer.replace("obj11.html", next_obj)

    # Find and replace the viewer section in the current file
    # Match from <div class='item-view'> to the end of the pagination script
    current_viewer_pattern = re.compile(
        r"<div class='item-view'>.*?</script>\s*\n",
        re.DOTALL
    )

    new_content = current_viewer_pattern.sub(new_viewer + "\n\n\n\n\n\n\n\n", content)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated {html_file.name}")

print(f"\n✓ Updated {count} object pages")
