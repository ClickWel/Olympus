import struct, sys, base64, re, os

def parse_pcap(path):
    tcp_streams = {}

    with open(path, 'rb') as f:
        magic, ver_maj, ver_min, thiszone, sigfigs, snaplen, network = struct.unpack('<IHHiIII', f.read(24))
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', hdr)
            pkt_data = f.read(incl_len)
            if len(pkt_data) < incl_len:
                break
            if len(pkt_data) < 14:
                continue
            eth_type = struct.unpack('>H', pkt_data[12:14])[0]
            if eth_type != 0x0800:
                continue
            if len(pkt_data) < 34:
                continue
            ip_ihl = (pkt_data[14] & 0x0F) * 4
            ip_proto = pkt_data[23]
            ip_src = '.'.join(str(b) for b in pkt_data[26:30])
            ip_dst = '.'.join(str(b) for b in pkt_data[30:34])
            ip_payload = pkt_data[14+ip_ihl:]

            if ip_proto != 6 or len(ip_payload) < 20:
                continue
            src_port = struct.unpack('>H', ip_payload[0:2])[0]
            dst_port = struct.unpack('>H', ip_payload[2:4])[0]
            tcp_hdr_len = ((ip_payload[12] >> 4) & 0x0F) * 4
            tcp_payload = ip_payload[tcp_hdr_len:]
            if not tcp_payload:
                continue
            key = (ip_src, src_port, ip_dst, dst_port)
            seq = struct.unpack('>I', ip_payload[4:8])[0]
            if key not in tcp_streams:
                tcp_streams[key] = []
            tcp_streams[key].append((seq, tcp_payload))

    os.makedirs('D:/Olympus/ctf/attachments', exist_ok=True)
    part_num = 1

    for key, segments in tcp_streams.items():
        src, sport, dst, dport = key
        if dport != 25 and sport != 25:
            continue
        if src != '192.168.68.108':  # Only client sending emails
            continue
        segments.sort(key=lambda x: x[0])
        stream = b''
        for seq, payload in segments:
            stream += payload
        text = stream.decode('utf-8', errors='ignore')

        # Extract password
        pw_match = re.search(r'Password: (\S+)', text)
        if not pw_match:
            continue
        password = pw_match.group(1)
        print(f"Found email with password: {password}")

        # Extract base64 attachment
        b64_match = re.search(r'Content-Transfer-Encoding: base64\r\n(.*?)\r\n\r\n--', text, re.DOTALL)
        if not b64_match:
            continue
        b64_data = b64_match.group(1).replace('\r\n', '').strip()
        print(f"Base64 length: {len(b64_data)}")

        # Decode base64
        try:
            zip_data = base64.b64decode(b64_data)
        except Exception as e:
            print(f"Base64 decode failed: {e}")
            continue

        # Save zip file
        zip_path = f'D:/Olympus/ctf/attachments/part{part_num}.zip'
        with open(zip_path, 'wb') as f:
            f.write(zip_data)
        print(f"Saved {zip_path} ({len(zip_data)} bytes)")
        part_num += 1

        # Save password to file
        with open('D:/Olympus/ctf/attachments/passwords.txt', 'a') as f:
            f.write(f"part{part_num-1}.zip: {password}\n")

if __name__ == '__main__':
    parse_pcap(sys.argv[1])
