#!/usr/bin/env python3
import requests

# Try different ports from the run.sh
# run.sh has: hostfwd=tcp::1337-:1337, hostfwd=tcp::1338-:1338, hostfwd=tcp::31337-:31337
ports = [1337, 1338, 31337, 30817]

print("=== Testing different ports ===")
for port in ports:
    try:
        r = requests.get(f"http://154.57.164.66:{port}/", auth=("admin", "router123"), timeout=3)
        print(f"Port {port}: {r.status_code} - {r.text[:50] if r.status_code == 200 else 'N/A'}")
    except Exception as e:
        print(f"Port {port}: Error - {str(e)[:50]}")

# Also try without auth on each port
print("\n=== Without auth ===")
for port in ports:
    try:
        r = requests.get(f"http://154.57.164.66:{port}/", timeout=3)
        print(f"Port {port}: {r.status_code} - {r.text[:30] if 'Auth' not in r.text else 'Auth required'}")
    except Exception as e:
        print(f"Port {port}: Error - {str(e)[:50]}")