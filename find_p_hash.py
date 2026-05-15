#!/usr/bin/env python3
"""
Find $p$ context in firmware.
"""
import re

with open(r'C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin', 'rb') as f:
    data = f.read()

# Find $p$ occurrence
idx = data.find(b'$p$')
if idx >= 0:
    start = max(0, idx - 100)
    end = min(len(data), idx + 100)
    context = data[start:end]
    print(f"Context around $p$ (offset {idx}):")
    print(context)
    print()
    # Print all around it
    print("Full context as string:")
    print(context.decode('utf-8', errors='replace'))