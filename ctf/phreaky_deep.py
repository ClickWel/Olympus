import struct, sys, zlib, re

def parse_pcap(path):
    packets = []
    tcp_streams = {}  # (src, sport, dst, dport) -> list of (seq, payload)
    dns_queries = []

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

            # DNS (UDP 53)
            if ip_proto == 17 and len(ip_payload) >= 8:
                src_port = struct.unpack('>H', ip_payload[0:2])[0]
                dst_port = struct.unpack('>H', ip_payload[2:4])[0]
                udp_payload = ip_payload[8:]
                if src_port == 53 or dst_port == 53:
                    # Simple DNS parse: transaction ID (2), flags (2), qdcount (2)
                    if len(udp_payload) >= 12:
                        qdcount = struct.unpack('>H', udp_payload[4:6])[0]
                        # Skip header (12 bytes) and question section
                        # For simplicity, just log DNS packets
                        dns_queries.append((ip_src, src_port, ip_dst, dst_port, len(udp_payload)))

            # TCP
            if ip_proto == 6 and len(ip_payload) >= 20:
                src_port = struct.unpack('>H', ip_payload[0:2])[0]
                dst_port = struct.unpack('>H', ip_payload[2:4])[0]
                tcp_hdr_len = ((ip_payload[12] >> 4) & 0x0F) * 4
                tcp_payload = ip_payload[tcp_hdr_len:]
                if tcp_payload:
                    key = (ip_src, src_port, ip_dst, dst_port)
                    seq = struct.unpack('>I', ip_payload[4:8])[0]
                    if key not in tcp_streams:
                        tcp_streams[key] = []
                    tcp_streams[key].append((seq, tcp_payload))

    # Print DNS summary
    print("=== DNS Activity ===")
    for q in dns_queries[:20]:
        print(f"DNS: {q[0]}:{q[1]} -> {q[2]}:{q[3]} len {q[4]}")

    # Reassemble TCP streams
    print("\n=== TCP Streams ===")
    for key, segments in tcp_streams.items():
        src, sport, dst, dport = key
        # Sort by sequence number
        segments.sort(key=lambda x: x[0])
        # Merge payloads (simple, no retransmission handling)
        stream = b''
        for seq, payload in segments:
            stream += payload
        print(f"Stream {src}:{sport} -> {dst}:{dport} total {len(stream)} bytes")

        # Check for HTTP
        if stream.startswith(b'HTTP/') or stream.startswith(b'GET ') or stream.startswith(b'POST '):
            print(f"  HTTP traffic detected")
            # Try to decompress if gzipped
            if stream.startswith(b'HTTP/'):
                # Extract body after \r\n\r\n
                headers_end = stream.find(b'\r\n\r\n')
                if headers_end != -1:
                    body = stream[headers_end+4:]
                    # Check for gzip
                    if b'Content-Encoding: gzip' in stream[:headers_end]:
                        try:
                            body = zlib.decompress(body, 16+zlib.MAX_WBITS)
                            print(f"  Decompressed gzip body: {len(body)} bytes")
                        except:
                            pass
                    # Print first 500 bytes of body
                    print(f"  Body preview: {body[:500]}")

        # Check for any text/strings
        if len(stream) > 0:
            strings = re.findall(b'[ -~\s]{8,}', stream)
            if strings:
                print(f"  Strings found: {[s.decode('utf-8', errors='ignore')[:50] for s in strings[:5]]}")

    print(f"\nTotal DNS packets: {len(dns_queries)}")
    print(f"Total TCP streams: {len(tcp_streams)}")

if __name__ == '__main__':
    parse_pcap(sys.argv[1])
