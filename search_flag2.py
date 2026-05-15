#!/usr/bin/env python3
"""
Search for flag_boot strings.
"""
import re

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Find all occurrences of flag_boot
pattern = rb'flag_boot_\w+'
matches = list(re.finditer(pattern, data))
print(f"Found {len(matches)} flag_boot patterns:")
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(data), m.end() + 100)
    context = data[start:end]
    print(f"\nOffset {m.start()}:")
    print(context)