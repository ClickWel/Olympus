#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

try:
    r = requests.get(f"{URL}/", auth=AUTH, timeout=5)
    print(f"Root: {r.status_code}")
    
    r = requests.get(f"{URL}/admin", auth=AUTH, timeout=5)
    print(f"Admin: {r.status_code}")
except Exception as e:
    print(f"Error: {e}")