#!/usr/bin/env python3
# Find all references to dev mode check

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# The dev_mode_enabled variable is around 10642383
# Let's look for patterns that might indicate how it's checked

# Look for "dev_mode" in the error context (around 6019884)
dev_error_zone = data[6000000:6100000]
print("=== Strings near Dev Mode error ===")

# Find null-terminated strings
i = 0
while i < len(dev_error_zone) - 4:
    # Look for printable sequences
    if dev_error_zone[i] >= 32 and dev_error_zone[i] < 127:
        j = i
        while j < len(dev_error_zone) and dev_error_zone[j] >= 32 and dev_error_zone[j] < 127 and dev_error_zone[j] != 0:
            j += 1
        if j - i > 5:
            s = dev_error_zone[i:j].decode('utf-8', errors='replace')
            if 'admin' in s.lower() or 'dev' in s.lower() or 'ping' in s.lower() or 'mode' in s.lower():
                print(f"  {i+6000000}: {s}")
        i = j
    else:
        i += 1

# Look for function that checks dev mode
print("\n=== Looking for dev mode check logic ===")
check_patterns = [b'dev_mode_enabled', b'DevMode', b'devMode', b'isDevMode', b'IsDev']
for pat in check_patterns:
    pos = data.find(pat, 6000000)
    while pos >= 6000000 and pos < 6100000:
        context = data[max(6000000,pos-100):min(6100000,pos+100)].decode('utf-8', errors='replace')
        print(f"Found '{pat.decode()}' at {pos}: {context}")
        pos = data.find(pat, pos+1)