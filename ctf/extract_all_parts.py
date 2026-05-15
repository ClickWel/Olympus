import struct, sys, base64, re, os

def get_all_tcp_streams(path, target_src='192.168.68.108', target_dport=25):
    streams = {}
    with open(path, 'rb') as f:
        f.read(24)  # skip global header
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
            if key not in streams:
                streams[key] = []
            streams[key].append((seq, tcp_payload))
    # Return all matching streams
    result = []
    for key, segs in streams.items():
        src, sport, dst, dport = key
        if src == target_src and dport == target_dport:
            segs.sort(key=lambda x: x[0])
            result.append(b''.join(p for s, p in segs))
    return result

def extract_parts_from_stream(text, part_offset=0):
    emails = re.split(r'(?=HELO phreak-ubuntu01)', text)
    extracted = []
    part = part_offset + 1
    for email in emails:
        if 'Content-Transfer-Encoding: base64' not in email:
            continue
        pw_match = re.search(r'Password: (\S+)', email)
        if not pw_match:
            continue
        password = pw_match.group(1)
        bound_match = re.search(r'boundary="(.*?)"', email)
        if not bound_match:
            continue
        boundary = bound_match.group(1)
        b64_header = email.find('Content-Transfer-Encoding: base64')
        if b64_header == -1:
            continue
        blank = email.find('\n\n', b64_header)
        if blank == -1:
            blank = email.find('\r\n\r\n', b64_header)
        if blank == -1:
            continue
        b64_start = blank + 2
        b64_end = email.find(f'--{boundary}', b64_start)
        if b64_end == -1:
            continue
        b64_content = email[b64_start:b64_end].strip()
        b64_clean = re.sub(r'\s+', '', b64_content)
        print(f"Part {part}: password {password}, b64 length {len(b64_clean)}")
        try:
            data = base64.b64decode(b64_clean)
        except Exception as e:
            print(f"Decode failed: {e}")
            part += 1
            continue
        if data[:4] != b'PK\x03\x04':
            print("Not a zip file")
            part += 1
            continue
        extracted.append((part, password, data))
        print(f"Decoded part {part}: {len(data)} bytes")
        part += 1
    return extracted

def main():
    pcap_path = sys.argv[1]
    streams = get_all_tcp_streams(pcap_path)
    print(f"Found {len(streams)} TCP streams from client to SMTP server")
    os.makedirs('D:/Olympus/ctf/parts', exist_ok=True)
    all_parts = []
    for i, stream in enumerate(streams):
        text = stream.decode('utf-8', errors='ignore')
        parts = extract_parts_from_stream(text, len(all_parts))
        all_parts.extend(parts)
    print(f"\nTotal parts extracted: {len(all_parts)}")
    for part_num, password, data in all_parts:
        zip_path = f'D:/Olympus/ctf/parts/part{part_num}.zip'
        with open(zip_path, 'wb') as f:
            f.write(data)
        print(f"Saved {zip_path}")
    # Save passwords
    with open('D:/Olympus/ctf/parts/passwords.txt', 'w') as f:
        for part_num, password, data in all_parts:
            f.write(f"part{part_num}.zip: {password}\n")

if __name__ == '__main__':
    main()
