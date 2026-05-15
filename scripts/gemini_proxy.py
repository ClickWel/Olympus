import json
import os
import sys
import http.server
import socketserver
import urllib.request
import urllib.error
import base64

PORT = 4444

GEMINI_KEY = None
env_path = r'D:\Olympus\MASTER_API_KEYS.env'
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('GOOGLE_API_KEY=') or line.startswith('GOOGLE_GENERATIVE_AI_API_KEY='):
                GEMINI_KEY = line.strip().split('=', 1)[1]
                break

if not GEMINI_KEY:
    print("ERROR: No GOOGLE_API_KEY found in D:\Olympus\MASTER_API_KEYS.env")
    sys.exit(1)

print("Proxy ready on http://localhost:" + str(PORT))
print("Key: " + GEMINI_KEY[:10] + "...")
