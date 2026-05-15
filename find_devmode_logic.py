#!/usr/bin/env python3
# Find strings related to dev mode check and routing

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Search around the enable_dev_mode function for context
dev_mode_func = data.find(b'enable_dev_mode')
if dev_mode_func >= 0:
    print(f"=== Around enable_dev_mode at offset {dev_mode_func} ===")
    context = data[dev_mode_func-200:dev_mode_func+500].decode('utf-8', errors='replace')
    print(context)

dev_mode_enabled = data.find(b'dev_mode_enabled')
if dev_mode_enabled >= 0:
    print(f"\n=== Around dev_mode_enabled at offset {dev_mode_enabled} ===")
    context = data[dev_mode_enabled-200:dev_mode_enabled+300].decode('utf-8', errors='replace')
    print(context)

# Look for the "Dev Mode Not Enabled" error message
error_msg = data.find(b'Dev Mode Not Enabled')
if error_msg >= 0:
    print(f"\n=== Around error message at offset {error_msg} ===")
    context = data[error_msg-200:error_msg+300].decode('utf-8', errors='replace')
    print(context)