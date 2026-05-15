#!/usr/bin/env python3
# Search for the enable_dev_mode function references

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Find enable_dev_mode function
enable_func = data.find(b'enable_dev_mode')
if enable_func >= 0:
    print(f"=== enable_dev_mode at {enable_func} ===")
    # Look for cross-references - functions that call enable_dev_mode
    # In the binary, look for calls to this function
    
    # Also look for what might call it - search for patterns like "Enabling"
    enabling_msg = data.find(b'Enabling; Previous Dev Mode:')
    if enabling_msg >= 0:
        print(f"=== Enabling message at {enabling_msg} ===")
        # This looks like a printf/cout statement - let's see what's around it
        context = data[enabling_msg-1000:enabling_msg+500].decode('utf-8', errors='replace')
        # Clean for display
        clean = ''.join(c if c.isprintable() else '.' for c in context)
        print(clean[:1500])