import struct, sys

def parse_pcap(path):
    tcp_streams = {}  # (src, sport, dst, dport) -> list of (seq, payload)

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
            # Parse Ethernet
            if len(pkt_data) < 14:
                continue
            eth_type = struct.unpack('>H', pkt_data[12:14])[0]
            if eth_type != 0x0800:
                continue
            # Parse IP
            if len(pkt_data) < 34:
                continue
            ip_ihl = (pkt_data[14] & 0x0F) * 4
            ip_proto = pkt_data[23]
            ip_src = '.'.join(str(b) for b in pkt_data[26:30])
            ip_dst = '.'.join(str(b) for b in pkt_data[30:34])
            ip_payload = pkt_data[14+ip_ihl:]

            # TCP only
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

    # Extract SMTP streams (port 25)
    print("=== Extracting SMTP Streams ===")
    for key, segments in tcp_streams.items():
        src, sport, dst, dport = key
        if dport != 25 and sport != 25:
            continue
        # Sort by sequence number
        segments.sort(key=lambda x: x[0])
        stream = b''
        for seq, payload in segments:
            stream += payload
        # Decode as text
        try:
            text = stream.decode('utf-8', errors='ignore')
        except:
            text = stream.decode('latin-1', errors='ignore')
        print(f"\n=== Stream {src}:{sport} -> {dst}:{dport} ({len(stream)} bytes) ===")
        print(text[:2000])  # Print first 2000 chars

if __name__ == '__main__':
    parse_pcap(sys.argv[1])
