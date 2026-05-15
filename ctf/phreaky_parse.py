import struct, sys

def parse_pcap(path):
    with open(path, 'rb') as f:
        # PCAP global header: 24 bytes
        magic, ver_maj, ver_min, thiszone, sigfigs, snaplen, network = struct.unpack('<IHHiIII', f.read(24))
        print(f"PCAP magic: {hex(magic)}, version {ver_maj}.{ver_min}, snaplen {snaplen}, link type {network}")
        # Link type 1 = Ethernet
        pkt_count = 0
        while True:
            # Packet header: 16 bytes (ts sec, ts usec, incl len, orig len)
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', hdr)
            pkt_data = f.read(incl_len)
            if len(pkt_data) < incl_len:
                break
            pkt_count += 1
            # Parse Ethernet header (14 bytes)
            if len(pkt_data) < 14:
                continue
            eth_dst = pkt_data[0:6].hex(':')
            eth_src = pkt_data[6:12].hex(':')
            eth_type = struct.unpack('>H', pkt_data[12:14])[0]
            # Parse IP if eth_type 0x0800
            if eth_type == 0x0800 and len(pkt_data) >= 34:
                ip_ver_ihl = pkt_data[14]
                ip_proto = pkt_data[23]
                ip_src = '.'.join(str(b) for b in pkt_data[26:30])
                ip_dst = '.'.join(str(b) for b in pkt_data[30:34])
                proto_map = {6: 'TCP', 17: 'UDP', 1: 'ICMP'}
                proto = proto_map.get(ip_proto, str(ip_proto))
                # Parse UDP/TCP ports
                if ip_proto == 17 and len(pkt_data) >= 42:  # UDP
                    src_port = struct.unpack('>H', pkt_data[34:36])[0]
                    dst_port = struct.unpack('>H', pkt_data[36:38])[0]
                    print(f"Packet {pkt_count}: {ip_src}:{src_port} -> {ip_dst}:{dst_port} UDP len {incl_len}")
                elif ip_proto == 6 and len(pkt_data) >= 44:  # TCP
                    src_port = struct.unpack('>H', pkt_data[34:36])[0]
                    dst_port = struct.unpack('>H', pkt_data[36:38])[0]
                    print(f"Packet {pkt_count}: {ip_src}:{src_port} -> {ip_dst}:{dst_port} TCP len {incl_len}")
            elif eth_type == 0x0806:  # ARP
                print(f"Packet {pkt_count}: ARP")
            else:
                print(f"Packet {pkt_count}: Eth type {hex(eth_type)} len {incl_len}")
    print(f"Total packets: {pkt_count}")

if __name__ == '__main__':
    parse_pcap(sys.argv[1])
