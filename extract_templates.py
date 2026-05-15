#!/usr/bin/env python3
import re

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Extract all mustache templates
print("=== All HTML/template blocks ===")
# Find all <!DOCTYPE html occurrences
pos = 0
count = 0
while count < 10:
    pos = data.find(b'<!DOCTYPE html', pos)
    if pos < 0:
        break
    # Get about 4KB of content
    content = data[pos:pos+8000].decode('utf-8', errors='replace')
    # Clean up non-printable chars for display
    clean = ''.join(c if c.isprintable() or c in '\n\r\t' else '?' for c in content)
    print(f"\n--- Block at offset {pos} ---")
    print(clean[:1500])
    pos += 1
    count += 1

# Also look for index.mustache or similar template references
print("\n\n=== Looking for template file references ===")
for pattern in [b'.mustache', b'template', b'index.', b'home']:
    matches = re.findall(rb'[\w/]+\.mustache|[\w/]+\.html|[\w/]+' + pattern, data)
    for m in set(matches):
        if len(m) > 5:
            print(f"Found: {m.decode(errors='replace')}")