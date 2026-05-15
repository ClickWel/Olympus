#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# From the binary routes:
# /configs/use/<string>

# Try with trailing slash
for path in ["/configs/use/test/", "/configs/use/dev/", "/configs/use/Default/"]:
    r = requests.get(f"{URL}{path}", auth=AUTH, timeout=3)
    print(f"GET {path}: {r.status_code}")

# Check if maybe the route is actually /use/<string> (not /configs/use/<string>)
print("\n=== Check routes from HTML ===")
r = requests.get(f"{URL}/configs", auth=AUTH, timeout=5)
# Extract all links from HTML
import re
links = re.findall(r'href="(/[^"]+)"', r.text)
for link in sorted(set(links)):
    if 'use' in link or 'delete' in link:
        r2 = requests.get(f"{URL}{link}", auth=AUTH, timeout=3)
        print(f"GET {link}: {r2.status_code}")