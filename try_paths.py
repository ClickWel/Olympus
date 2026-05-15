#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# From HTML: <a href="/use/test" class="btn btn-secondary">Use This Config</a>
# But the route list shows: /configs/use/<string>
# Let me try both

paths = [
    "/use/test",
    "/use/dev", 
    "/use/Default",
    "/configs/use/test",
    "/configs/use/dev",
    "/configs/use/Default",
]

for path in paths:
    r = requests.get(f"{URL}{path}", auth=AUTH, timeout=3)
    print(f"GET {path}: {r.status_code} - {r.text[:50] if r.status_code != 404 else 'Not found'}")