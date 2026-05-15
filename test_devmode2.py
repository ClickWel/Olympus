#!/usr/bin/env python3
import requests

URL = "http://154.57.164.66:30817"
AUTH = ("admin", "router123")

# Try various dev mode enabling methods
methods = [
    # POST methods
    ("POST", "/enable", {"devMode": "true"}),
    ("POST", "/devmode", {"enable": "true"}),
    ("POST", "/admin/dev", {"enabled": "1"}),
    ("POST", "/setup", {"devMode": "true"}),
    ("POST", "/init", {"devMode": "true"}),
    ("POST", "/start", {"devMode": "true"}),
    
    # GET with params
    ("GET", "/enable?devMode=true", {}),
    ("GET", "/devmode?enable=true", {}),
    ("GET", "/admin/enable?devMode=true", {}),
]

for method, path, data in methods:
    print(f"\n--- {method} {path} ---")
    try:
        if method == "POST":
            r = requests.post(f"{URL}{path}", auth=AUTH, data=data, timeout=10)
        else:
            r = requests.get(f"{URL}{path}", auth=AUTH, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code != 404 and "Not Found" not in r.text:
            print(r.text[:200])
    except Exception as e:
        print(f"Error: {e}")