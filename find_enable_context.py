#!/usr/bin/env python3

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Search for the "Enabling; Previous Dev Mode:" string and look backward for context
enabling_pos = data.find(b'Enabling; Previous Dev Mode:')
if enabling_pos >= 0:
    print(f"=== Found at offset {enabling_pos} ===")
    # Look at a larger context - maybe there's a route path before it
    context = data[enabling_pos-2000:enabling_pos+200].decode('utf-8', errors='replace')
    print(context)
    
# Also look for "Disabling"
disabling_pos = data.find(b'Disabling; Previous Dev Mode:')
if disabling_pos >= 0:
    print(f"\n=== Disabling found at offset {disabling_pos} ===")
    context = data[disabling_pos-2000:disabling_pos+200].decode('utf-8', errors='replace')
    print(context)