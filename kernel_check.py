#!/usr/bin/env python3
"""
Check kernel command line and boot parameters for password hints.
"""
import re

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Look for kernel command line patterns
cmdline_patterns = [
    rb'root=',
    rb'init=',
    rb'passwd',
    rb'password',
]

for pat in cmdline_patterns:
    matches = list(re.finditer(pat, data, re.IGNORECASE))
    print(f"{pat.decode()}: {len(matches)} matches")
    for m in matches[:5]:
        start = max(0, m.start() - 50)
        end = min(len(data), m.end() + 100)
        context = data[start:end]
        print(f"  {context}")