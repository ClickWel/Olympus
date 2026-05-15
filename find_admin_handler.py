#!/usr/bin/env python3
# Look for the exact route handling in the binary

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Search for the Admin route handler context
error_pos = data.find(b'Dev Mode Not Enabled')
if error_pos >= 0:
    # Get a larger context
    context = data[error_pos-500:error_pos+500].decode('utf-8', errors='replace')
    print("=== Around Dev Mode Not Enabled error ===")
    print(context)

# Also look for where dev_mode_enabled is used
dev_mode_pos = data.find(b'dev_mode_enabled\x00')
if dev_mode_pos >= 0:
    # Look for references to this variable
    context = data[dev_mode_pos-300:dev_mode_pos+300].decode('utf-8', errors='replace')
    print("\n=== Around dev_mode_enabled definition ===")
    print(context)