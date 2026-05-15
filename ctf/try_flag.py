import socket
import time

def try_various():
    # Try 1: Send "STOP DROP ROLL" at ready prompt
    print("=== Try 1: Send 'STOP DROP ROLL' at ready ===")
    s = socket.socket()
    s.settimeout(10)
    s.connect(('154.57.164.78', 32230))
    data = s.recv(4096).decode('utf-8', errors='ignore')
    print(data[:200])
    s.send(b'STOP DROP ROLL\n')
    time.sleep(0.5)
    data = s.recv(4096).decode('utf-8', errors='ignore')
    print(f"Response: {data[:300]}")
    if 'HTB{' in data:
        print(f"FLAG: {data}")
    s.close()
    
    time.sleep(1)
    
    # Try 2: Send wrong answers
    print("\n=== Try 2: Send wrong answers ===")
    s = socket.socket()
    s.settimeout(10)
    s.connect(('154.57.164.78', 32230))
    data = s.recv(4096)
    s.send(b'y\n')
    time.sleep(0.5)
    for i in range(5):
        data = s.recv(4096).decode('utf-8', errors='ignore')
        print(f"Round {i+1}: {data.strip()[:100]}")
        # Send wrong answer
        s.send(b'WRONG\n')
        time.sleep(0.3)
    data = s.recv(4096).decode('utf-8', errors='ignore')
    print(f"After wrong answers: {data[:300]}")
    if 'HTB{' in data:
        print(f"FLAG: {data}")
    s.close()
    
    time.sleep(1)
    
    # Try 3: Send "STOP DROP ROLL" as answer to first scenario
    print("\n=== Try 3: Send 'STOP DROP ROLL' as answer ===")
    s = socket.socket()
    s.settimeout(10)
    s.connect(('154.57.164.78', 32230))
    data = s.recv(4096)
    s.send(b'y\n')
    time.sleep(0.5)
    data = s.recv(4096).decode('utf-8', errors='ignore')
    print(f"First scenario: {data.strip()[:100]}")
    s.send(b'STOP DROP ROLL\n')
    time.sleep(0.5)
    data = s.recv(4096).decode('utf-8', errors='ignore')
    print(f"Response: {data[:300]}")
    if 'HTB{' in data:
        print(f"FLAG: {data}")
    s.close()

if __name__ == '__main__':
    try_various()
