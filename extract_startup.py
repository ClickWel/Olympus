#!/usr/bin/env python3
# Extract the full startup script and router-web-panel content

with open('D:/CTF/challenges/router-web/router_web/rootfs.ext2', 'rb') as f:
    data = f.read()

# Found at 5014603 - extract more context
pos = 5014603
print("=== Full startup script ===")
context = data[pos-200:pos+500].decode('utf-8', errors='replace')
print(context)

# Look for /usr/bin/router-web-panel - could be a binary or script
print("\n=== /usr/bin/router-web-panel content ===")
pos2 = data.find(b'/usr/bin/router-web-panel')
while pos2 >= 0:
    context = data[max(0,pos2-100):pos2+300].decode('utf-8', errors='replace')
    print(f"At {pos2}: {context}")
    pos2 = data.find(b'/usr/bin/router-web-panel', pos2+1)

# Check /opt/router-web-panel/run.sh
print("\n=== Checking /opt/router-web-panel/run.sh ===")
pos3 = data.find(b'/opt/router-web-panel/run.sh')
while pos3 >= 0:
    context = data[max(0,pos3-100):pos3+200].decode('utf-8', errors='replace')
    print(f"At {pos3}: {context}")
    pos3 = data.find(b'/opt/router-web-panel/run.sh', pos3+1)