#!/usr/bin/env python3
# Extract the S20router-web-panel script

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find S20router-web-panel
pos = data.find(b'S20router-web-panel')
if pos >= 0:
    print(f"=== Found at {pos} ===")
    # Get surrounding context to find the script content
    # The file structure suggests this is a symlink or script name in the inode table
    # Look backwards for script content
    context = data[pos-500:pos+500].decode('utf-8', errors='replace')
    print(context)
    
# Also look for router-web or the actual binary
print("\n=== Looking for router-web binary ===")
pos = data.find(b'router-web')
while pos >= 0:
    context = data[max(0,pos-100):pos+200].decode('utf-8', errors='replace')
    print(f"router-web at {pos}: {context[:200]}")
    pos = data.find(b'router-web', pos+1)