import socket, time, bcrypt

# Generate the correct hash deterministically
# Step 1: get a salt from gensalt
salt_original = bcrypt.gensalt(rounds=4)
print("Original salt:", salt_original)

# Step 2: construct the salt with JgiaOAai
# Format: $2b$04$<22-char-salt>
salt_str = salt_original.decode()
parts = salt_str.split('$')
print("Parts:", parts)
# parts[0] = '', parts[1] = '2b', parts[2] = '04', parts[3] = '<22-char-salt>'

# New salt (22 chars) starting with JgiaOAai
new_salt_22 = 'JgiaOAai..............'  # 8 + 14 = 22 chars
print("New salt (22 chars):", new_salt_22, "len=", len(new_salt_22))

# Reconstruct full salt param: $2b$04$JgiaOAai..............
new_salt_param = '$' + parts[1] + '$' + parts[2] + '$' + new_salt_22
print("New salt param:", new_salt_param)

# Step 3: hash empty password with this salt
try:
    hash_result = bcrypt.hashpw(b'\x00', new_salt_param.encode())
    print("Hash (2b$):", hash_result.decode())

    # Step 4: convert to $2$ format
    hash_2 = hash_result.decode().replace('$' + '2b$' , '$' + '2$')
    print("Hash ($2$):", hash_2)

    # Step 5: try different answer formats
    answers = [
        'root:' + hash_2,
        'root:' + hash_2 + ':0:99999:7:::',
        # Without cost parameter
        'root:$' + '2$' + new_salt_22 + hash_2[53:],  # 53 = len(new_salt_22) + 31
        'root:$' + '2$' + new_salt_22 + hash_2[53:] + ':0:99999:7:::',
    ]

    host = '154.57.164.61'
    port = 31539

    for i, answer in enumerate(answers, 1):
        print(f"\n=== Trying answer {i}: {answer[:60]}... ===")
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
            print(f"Response: {resp[:200]}")
            if 'Correct' in resp:
                print(f"SUCCESS! Answer: {answer}")
                break
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            s.close()
        time.sleep(3)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
