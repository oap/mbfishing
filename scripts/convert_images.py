#!/usr/bin/env python3
import os
from PIL import Image

SRC_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
SRC_DIR = os.path.abspath(SRC_DIR)

converted = []
skipped = []
errors = []

for root, _, files in os.walk(SRC_DIR):
    for fn in files:
        name, ext = os.path.splitext(fn)
        if ext.lower() not in ('.png', '.jpg', '.jpeg'):
            continue
        src = os.path.join(root, fn)
        dest = os.path.join(root, name + '.webp')
        if os.path.exists(dest):
            skipped.append(dest)
            continue
        try:
            with Image.open(src) as im:
                # Preserve transparency when possible
                mode = 'RGBA' if im.mode in ('RGBA','LA') else 'RGB'
                im = im.convert(mode)
                im.save(dest, 'WEBP', quality=85, method=6)
            converted.append(dest)
        except Exception as e:
            errors.append((src, str(e)))

print('Converted:', len(converted))
for p in converted:
    print('  +', p)
print('Skipped (already exist):', len(skipped))
print('Errors:', len(errors))
for src, msg in errors:
    print('  !', src, msg)
