#!/usr/bin/env python3
"""
Search for the example pattern from the challenge hint.
Example: root:$2$JgiaOAai....
"""
import re

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Search for JgiaOAai pattern from example
matches = list(re.finditer(rb'JgiaOAai', data))
print(f"Matches for JgiaOAai: {len(matches)}")

# Search for the pattern with root:
matches = list(re.finditer(rb'root:\$2\$', data))
print(f"Matches for root:$2$: {len(matches)}")

# Full firmware search for any $2$ followed by text
matches = list(re.finditer(rb'\$2\$[a-zA-Z0-9./]{20,}', data))
print(f"Matches for $2$... pattern: {len(matches)}")
for m in matches:
    print(f"  {m.group().decode('utf-8', errors='replace')}")

# Also check if the answer might be in the SquashFS somewhere else
import os
squashfs_root = r'D:\Olympus\SquashFS_root'
for root, dirs, files in os.walk(squashfs_root):
    for f in files:
        filepath = os.path.join(root, f)
        try:
            with open(filepath, 'rb') as fh:
                content = fh.read()
            if b'$2$' in content:
                print(f"Found $2$ in: {filepath}")
        except:
            pass