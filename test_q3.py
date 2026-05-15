#!/usr/bin/env python3
"""Test Q3 answers against the CTF server."""
import socket
import time

def interact(host, port, answers):
    """Send answers to Q3 and check responses."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(15)
    s.connect((host, port))
    time.sleep(0.5)

    # Read banner
    data = b''
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
    except socket.timeout: pass
    print("Banner received, length:", len(data))

    # Answer Q1
    s.sendall(b'23.05.0\n')
    time.sleep(0.3)
    try:
        resp = s.recv(4096)
        print("Q1 response:", resp.decode('utf-8', errors='replace')[:100])
    except: pass

    # Answer Q2
    s.sendall(b'5.15.134\n')
    time.sleep(0.3)
    try:
        resp = s.recv(4096)
        print("Q2 response:", resp.decode('utf-8', errors='replace')[:200])
    except: pass

    # Now at Q3 - read prompt
    time.sleep(0.3)
    try:
        prompt = s.recv(4096)
        print("Q3 prompt:", prompt.decode('utf-8', errors='replace')[:200])
    except: pass

    # Try each answer
    for ans in answers:
        print(f"\nTrying: {ans[:60]}...")
        s.sendall(ans.encode() + b'\n')
        time.sleep(0.5)
        try:
            resp = s.recv(4096)
            print("Response:", resp.decode('utf-8', errors='replace')[:200])
        except socket.timeout:
            print("Timeout - no response")
        time.sleep(0.5)

    s.close()

# Generate answers with bcrypt
import bcrypt

answers = []

# Helper: create proper salt bytes and encode to 22-char b64
BCRYPT_B64 = b'./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

def to_b64(data):
    result = []
    for i in range(0, len(data), 3):
        b1 = data[i]
        b2 = data[i+1] if i+1 < len(data) else 0
        b3 = data[i+2] if i+2 < len(data) else 0
        result.append(chr(BCRYPT_B64[b1 >> 2]))
        result.append(chr(BCRYPT_B64[((b1 & 0x03) << 4) | (b2 >> 4)]))
        if i+1 < len(data):
            result.append(chr(BCRYPT_B64[((b2 & 0x0F) << 2) | (b3 >> 6)]))
        if i+2 < len(data):
            result.append(chr(BCRYPT_B64[b3 & 0x3F]))
    return ''.join(result)

# Generate with different salts and costs
for cost in [4, 5, 6]:
    for salt_desc, salt_bytes in [
        ('zero', b'\x00' * 16),
        ('JgiaOAai+zero', b'\x2e\x29\x1c\x40\x29\x1c' + b'\x00' * 10),
        ('all_A', b'\x00' * 16),  # same as zero since A=0 in bcrypt b64
    ]:
        salt_b64 = to_b64(salt_bytes)
        salt_param = f'$2a${cost:02d}${salt_b64}'.encode()
        h = bcrypt.hashpw(b'\x00', salt_param)  # empty string + null
        h_str = h.decode().replace('$2a$', '$2$', 1)
        answers.append(f'root:{h_str}')

# Also try: what if the answer is just the shadow line itself?
answers.append('root:::0:99999:7:::')
answers.append('root:::')

# Try with password "root" instead of empty
for cost in [4, 5, 6]:
    salt_bytes = b'\x00' * 16
    salt_b64 = to_b64(salt_bytes)
    salt_param = f'$2a${cost:02d}${salt_b64}'.encode()
    h = bcrypt.hashpw(b'root\x00', salt_param)
    h_str = h.decode().replace('$2a$', '$2$', 1)
    answers.append(f'root:{h_str}')

print(f"Generated {len(answers)} answers to try")
for a in answers:
    print(f"  {a[:70]}...")

# Now test against server
print("\n\nTesting against server...")
interact('154.57.164.64', 31871, answers[:5])  # Try first 5 only
