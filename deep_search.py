#!/usr/bin/env python3
"""
Deep search for hash or password in firmware.
"""
import re
import os

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Search for all printable strings that could be passwords
strings = re.findall(rb'[\x20-\x7e]{16,80}', data)

password_candidates = []
for s in strings:
    s_str = s.decode('utf-8', errors='replace')
    # Look for things that could be bcrypt parts
    if '$' in s_str or 'root' in s_str.lower() or 'pass' in s_str.lower():
        password_candidates.append(s_str)

print("Password-related strings:")
for c in password_candidates[:50]:
    print(f"  {c[:100]}")

# Also check SquashFS for any file we might have missed
squashfs_root = r'D:\Olympus\SquashFS_root'
for root, dirs, files in os.walk(squashfs_root):
    for f in files:
        if 'passwd' in f.lower() or 'shadow' in f.lower() or 'secret' in f.lower():
            print(f"\nFound relevant file: {os.path.join(root, f)}")
            with open(os.path.join(root, f), 'rb') as fh:
                content = fh.read()
                print(content[:500])