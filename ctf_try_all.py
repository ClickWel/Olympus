#!/usr/bin/env python3
import socket, time

def send_answers(host, port, q3_hash):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(20)
    s.connect((host, port))
    time.sleep(1)
    # Discard banner
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            time.sleep(0.2)
        except: break
    # Q1
    s.sendall(b'23.05.0\n')
    time.sleep(1)
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            time.sleep(0.2)
        except: break
    # Q2
    s.sendall(b'5.15.134\n')
    time.sleep(1)
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            time.sleep(0.2)
        except: break
    # Q3
    ans = (q3_hash + '\n').encode('utf-8')
    print(f'Sending Q3: {ans}')
    s.sendall(ans)
    time.sleep(2)
    data = b''
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
            time.sleep(0.2)
        except: break
    resp = data.decode('utf-8', errors='replace')
    print(f'Response: {resp}')
    s.close()
    return 'Correct' in resp

if __name__ == '__main__':
    host = '154.57.164.61'
    port = 31539
    # Hashes to try (cost 4,5,6 with JgiaOAai salt)
    hashes = [
        'root:$2$04$JgiaOAai..............4v9t/DE.2LT4Ew5AldH8EPxpgxyI36W',
        'root:$2$05$JgiaOAai..............Nd.Bgi6fWXaEKIZf8qKhMbS9AFK5bKy',
        'root:$2$06$JgiaOAai..............ydfdSG.dqeUwIfy/emlNHLyYbWC0qn6',
        # Try zero salt
        'root:$2$04$......................w74bL5gU7LSJClZClCa.Pkz14aTv/XO',
        'root:$2$05$......................2vI5L1MdAJVA6dGvOaG0t./Ne5FBGm',
        'root:$2$06$......................qO6IuztV1K0sjw0Kq5kHonbzZ0FGfW',
    ]
    for h in hashes:
        print(f'\nTrying hash: {h[:30]}...')
        if send_answers(host, port, h):
            print('SUCCESS!')
            break
        time.sleep(5)  # Rate limit delay
