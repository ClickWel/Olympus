import socket
import time

HOST = "154.57.164.81"
PORT = 30714

def recv_all(s, timeout=10):
    s.settimeout(timeout)
    data = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            time.sleep(0.1)
        except socket.timeout:
            break
    return data.decode("utf-8", errors="replace")

def send_all(s, msg):
    s.sendall(msg.encode("utf-8"))
    time.sleep(0.5)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Connecting to {HOST}:{PORT}...")
    s.connect((HOST, PORT))

    # Read initial banner and Q1 prompt
    data = recv_all(s)
    print("Banner + Q1 prompt:\n" + data)

    # Answer Q1
    send_all(s, "23.05.0\n")
    data = recv_all(s)
    print("Q1 response:\n" + data)

    # Answer Q2
    send_all(s, "5.15.134\n")
    data = recv_all(s)
    print("Q2 response + Q3 prompt:\n" + data)

    # Answer Q3 with exact shadow line
    q3_answer = "root:::0:99999:7::::"
    print(f"\nSending Q3 answer: {q3_answer}")
    send_all(s, q3_answer + "\n")
    time.sleep(2)
    data = recv_all(s, timeout=15)
    print("Q3 response:\n" + data)

    # If it's wrong, try other variants
    if "Wrong" in data or "Incorrect" in data:
        variants = [
            "root:::0:99999:7:::\n",
            "root::0:99999:7:::",
            "root:::0:99999:7:::",
            "",
            "no password set",
            "$p$root"
        ]
        for v in variants:
            print(f"\nTrying variant: '{v}'")
            send_all(s, v + "\n")
            time.sleep(1)
            data = recv_all(s, timeout=5)
            print("Response: " + data.strip())
            if "Correct" in data:
                print("SUCCESS!")
                break