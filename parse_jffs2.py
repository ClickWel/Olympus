import struct

JFFS2_MAGIC = 0x1985
JFFS2_NODETYPE_INODE = 0xe002
JFFS2_NODETYPE_DIRENT = 0xe001

def parse_jffs2(jffs2_data):
    pos = 0
    inodes = {}  # inode -> list of (offset, data)
    dirents = {}  # name -> inode

    while pos < len(jffs2_data) - 12:
        # Read node header (big-endian)
        magic, nodetype, totlen, hdr_crc = struct.unpack('>HHII', jffs2_data[pos:pos+12])
        if magic != JFFS2_MAGIC:
            pos += 4
            continue

        if nodetype == JFFS2_NODETYPE_INODE and totlen >= 12 + 34:
            # Inode node: contains file data
            inode, version, mode, uid, gid, isize, atime, mtime, ctime, offset, compr, dsize, csize, payload_crc, name_crc = \
                struct.unpack('>IIHIIIIIIIBBHII', jffs2_data[pos+12:pos+12+34])
            data = jffs2_data[pos+12+34:pos+totlen]
            if inode not in inodes:
                inodes[inode] = b''
            inodes[inode] += data
            if b'shadow' in data or (offset == 0 and compr == 0):
                print(f"Inode {inode} (shadow?): {len(data)} bytes, offset {offset}")

        elif nodetype == JFFS2_NODETYPE_DIRENT and totlen >= 12 + 15:
            # Dirent node: directory entry
            pino, version, inode, type, name_crc, node_crc = \
                struct.unpack('>IIIBBH', jffs2_data[pos+12:pos+12+15])
            name_len = totlen - 12 - 15
            name = jffs2_data[pos+12+15:pos+12+15+name_len].rstrip(b'\x00').decode('utf-8', errors='replace')
            if 'shadow' in name or 'passwd' in name:
                print(f"Dirent: {name} -> inode {inode}")
            dirents[name] = inode

        pos += totlen
        if totlen < 12:
            pos += 12 - totlen

    return inodes, dirents

firmware_path = r"C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin"
with open(firmware_path, "rb") as f:
    f.seek(0x7c0000)
    jffs2_data = f.read(0x800000)  # 8MB

print(f"Parsing JFFS2 region ({len(jffs2_data)} bytes)...")
inodes, dirents = parse_jffs2(jffs2_data)

if 'shadow' in dirents:
    inode = dirents['shadow']
    print(f"\nFound shadow file (inode {inode}):")
    if inode in inodes:
        content = inodes[inode]
        print(content.decode('utf-8', errors='replace'))
    else:
        print("No data for inode")
else:
    print("\nshadow not in JFFS2 dirents. All dirents:")
    for name, inode in dirents.items():
        print(f"  {name} -> {inode}")