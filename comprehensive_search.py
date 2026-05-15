#!/usr/bin/env python3
"""
Comprehensive search for any hash or password in firmware.
Check both the original firmware AND try to understand what the server expects.
"""
import re
import os

# Check SquashFS for any hash-related files
squashfs_root = r'D:\Olympus\SquashFS_root'

print("Searching all files in SquashFS for potential password hashes...")

for root, dirs, files in os.walk(squashfs_root):
    for f in files:
        filepath = os.path.join(root, f)
        try:
            with open(filepath, 'rb') as fh:
                content = fh.read()

            # Look for hash-like patterns
            patterns = [
                rb'\$2\$',  # bcrypt old
                rb'\$2a\$', # bcrypt
                rb'\$2b\$', # bcrypt
                rb'\$1\$',  # MD5
                rb'\$5\$',  # SHA-256
                rb'\$6\$',  # SHA-512
            ]

            for pat in patterns:
                if pat in content:
                    print(f"Found {pat} in: {filepath}")
                    # Print context
                    idx = content.find(pat)
                    start = max(0, idx - 100)
                    end = min(len(content), idx + 200)
                    print(f"  Context: {content[start:end]}")
        except:
            pass

# Also check firmware binary for the example pattern
print("\nSearching firmware binary for the example salt JgiaOAai...")
with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Look for the exact example string
if b'JgiaOAai' in data:
    print("Found JgiaOAai in firmware!")
    idx = data.find(b'JgiaOAai')
    print(data[idx-50:idx+100])
else:
    print("JgiaOAai NOT found in firmware")