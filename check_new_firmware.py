#!/usr/bin/env python3
"""
Check if the new server has different firmware by:
1. Checking if it provides a firmware file
2. Looking for differences in the SquashFS
"""
import socket
import hashlib
import time

HOST = '154.57.164.73'
PORT = 31730

# Let's check if there's a way to get firmware from the server
# Some CTF challenges allow downloading the firmware via specific requests

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((HOST, PORT))

# Try various paths to see if we can get firmware
paths = [
    'GET /firmware.bin HTTP/1.1\r\nHost: localhost\r\n\r\n',
    'GET /squashfs.bin HTTP/1.1\r\nHost: localhost\r\n\r\n',
]

for path in paths:
    s.sendall(path.encode())
    time.sleep(0.5)
    try:
        data = s.recv(4096)
        print(f'Response for {path[:30]}...')
        print(data[:200])
    except:
        pass
    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))