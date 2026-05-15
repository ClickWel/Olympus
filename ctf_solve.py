#!/usr/bin/env python3
import socket, time

def interact(host, port, answers):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(20)
    s.connect((host, port))
    time.sleep(1)
    # Read banner
    data = b''
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
            time.sleep(0.2)
        except: break
    print('Banner received, length:', len(data))
    # Send answers
    for i, ans in enumerate(answers):
        print(f'Sending answer {i+1}: {ans}')
        s.sendall(ans.encode('utf-8') if isinstance(ans, str) else ans)
        time.sleep(1)
        # Read response
        data = b''
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk: break
                data += chunk
                time.sleep(0.2)
            except: break
        print(f'Response {i+1}:', data.decode('utf-8', errors='replace'))
    s.close()

if __name__ == '__main__':
    host = '154.57.164.61'
    port = 31539
    # Answers: Q1, Q2, Q3
    q3_hash = 'root:$2$04$JgiaOAai..............4v9t/DE.2LT4Ew5AldH8EPxpgxyI36W'
    answers = [
        '23.05.0',
        '5.15.134',
        q3_hash
    ]
    interact(host, port, answers)
