#!/usr/bin/env python3
"""
Search for flag_boot_root_pwd context in firmware.
"""
import re

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Find the flag_boot_root_pwd string and surrounding context
idx = data.find(b'flag_boot_root_pwd')
if idx >= 0:
    # Get 200 bytes before and after
    start = max(0, idx - 200)
    end = min(len(data), idx + 200)
    context = data[start:end]
    print(f"Context around flag_boot_root_pwd (offset {idx}):")
    print(context)
    print()
    # Also print as hex for non-printable chars
    print("As hex string:")
    print(context.hex())