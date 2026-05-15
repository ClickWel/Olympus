import socket, time, sys

HOST = '154.57.164.79'
PORT = 30582

def recv_all(s, timeout=5):
    data = b''
    s.settimeout(timeout)
    while True:
        try:
            chunk = s.recv(8192)
            if not chunk:
                break
            data += chunk
            time.sleep(0.1)
        except:
            break
    return data

s = socket.socket()
s.settimeout(15)
s.connect((HOST, PORT))
print('Connected.')

banner = recv_all(s)
print('=== BANNER ===')
print(banner.decode(errors='replace'))

s.close()
