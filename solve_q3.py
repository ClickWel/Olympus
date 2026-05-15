import socket, time, bcrypt

# Step 1: get a valid salt from gensalt
salt = bcrypt.gensalt(rounds=4)
print('Gensalt salt:', salt)

# Step 2: modify the salt to use JgiaOAai
salt_str = salt.decode()
parts = salt_str.split('$')
print('Parts:', parts)
# parts = ['', '2b', '04', '<22-char-salt>']
new_salt_22 = 'JgiaOAai..............'  # 22 chars
print('New salt (22 chars):', new_salt_22, 'len=', len(new_salt_22))
new_salt_str = '$' + parts[1] + '$' + parts[2] + '$' + new_salt_22
print('New full salt:', new_salt_str)

# Step 3: hash empty password with this salt
try:
    hash_result = bcrypt.hashpw(b'\x00', new_salt_str.encode())
    print('Hash result:', hash_result.decode())
    # Convert $2b$ to $2$
    hash_2 = hash_result.decode().replace('$2b$', '$2$', 1)
    print('As $2$:', hash_2)
    print('Full line: root:' + hash_2)
except Exception as e:
    print('Error generating hash:', e)
    import sys
    sys.exit(1)

# Step 4: submit to server
host = '154.57.164.61'
port = 31539

answers = [
    'root:' + hash_2,
    'root:' + hash_2 + ':0:99999:7:::',
]

for i, answer in enumerate(answers, 1):
    print(f'\n=== Trying answer {i}: {answer[:60]}... ===')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(20)
    try:
        s.connect((host, port))
        time.sleep(1)
        # Discard banner
        d = b''
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk: break
                d += chunk
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
        s.sendall((answer + '\n').encode())
        time.sleep(2)
        d = b''
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk: break
                d += chunk
                time.sleep(0.2)
            except: break
        resp = d.decode('utf-8', errors='replace')
        print(f'Response: {resp[:200]}')
        if 'Correct' in resp:
            print(f'SUCCESS! Answer: {answer}')
            break
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
    finally:
        s.close()
    time.sleep(3)
