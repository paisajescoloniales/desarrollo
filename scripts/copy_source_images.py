#!/usr/bin/env python3
"""Copy full-size images to use as IIIF source images"""

import os
import shutil
from pathlib import Path

# Find all full-size images
derivatives_dir = Path("img/derivatives/iiif/images")
source_dir = Path("components/images")
source_dir.mkdir(parents=True, exist_ok=True)

copied = 0
for img_path in derivatives_dir.glob("*/full/full/0/default.jpg"):
    # Extract object ID from path (e.g., obj10, obj35_6)
    obj_id = img_path.parts[3]  # img/derivatives/iiif/images/OBJ_ID/full/full/0/default.jpg

    # Copy to components/images/
    dest = source_dir / f"{obj_id}.jpg"
    shutil.copy2(img_path, dest)
    copied += 1
    print(f"Copied {obj_id}.jpg")

print(f"\n✓ Copied {copied} source images to {source_dir}")
