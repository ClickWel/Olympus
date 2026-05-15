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
    print("Connected. Reading initial banner...")
    initial = recv_all(s)
    print("Initial banner:\n" + initial)

    # Answer Q1 and Q2 first (confirmed working)
    if "Q1" in initial or "version" in initial.lower():
        print("\nSending Q1 answer: 23.05.0")
        send_all(s, "23.05.0\n")
        time.sleep(1)
        resp = recv_all(s)
        print("Q1 response:\n" + resp)

        print("\nSending Q2 answer: 5.15.134")
        send_all(s, "5.15.134\n")
        time.sleep(1)
        resp = recv_all(s)
        print("Q2 response:\n" + resp)

        # Capture Q3 prompt
        print("\nQ3 prompt:\n" + resp)
        time.sleep(2)
        q3_extra = recv_all(s, timeout=5)
        if q3_extra:
            print("Q3 additional context:\n" + q3_extra)
    else:
        print("No Q1/Q2 prompts detected in initial banner.")
