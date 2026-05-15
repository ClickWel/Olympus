#!/usr/bin/env python3
"""
Search for any password-related strings in firmware.
"""
import re

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Search for strings that look like password placeholders or hashes
patterns = [
    rb'password[=:]\s*\S+',
    rb'passwd[=:]\s*\S+',
    rb'root[=:]\s*\S+',
    rb'shadow[=:]\s*\S+',
    rb'\$p\$',  # OpenWrt password format
    rb'\$2\$',  # bcrypt old format
]

for pat in patterns:
    matches = re.findall(pat, data, re.IGNORECASE)
    if matches:
        print(f"Pattern {pat}: {len(matches)} matches")
        for m in matches[:10]:
            print(f"  {m}")