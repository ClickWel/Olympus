import re

firmware_path = r"C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin"

with open(firmware_path, "rb") as f:
    # uImage at 0x180000, read 0x1000 bytes
    f.seek(0x180000)
    uimage = f.read(0x1000)

    print("uImage header strings:")
    strings = re.findall(b'[\x20-\x7e]{8,}', uimage)
    for s in strings:
        print(s.decode('utf-8', errors='replace'))

    # Read JFFS2 region (0x7c0000) and scan for hashes
    f.seek(0x7c0000)
    jffs2 = f.read(0x100000)  # read 1MB of JFFS2
    print("\nJFFS2 region strings with 'root' or 'hash' or '$':")
    strings = re.findall(b'[\x20-\x7e]{8,}', jffs2)
    for s in strings:
        s_str = s.decode('utf-8', errors='replace')
        if any(k in s_str.lower() for k in ['root', 'hash', '$', 'password']):
            print(s_str)

    # Search entire firmware for '$2$JgiaOAai' (example hash prefix)
    print("\nSearching for example hash prefix '$2$JgiaOAai'...")
    f.seek(0)
    data = f.read()
    if b'$2$JgiaOAai' in data:
        print("Found example hash in firmware!")
    else:
        print("Example hash not in firmware.")

    # Search for any bcrypt hash in entire firmware
    print("\nSearching for any bcrypt ($2$) hashes in firmware...")
    bcrypt_matches = re.findall(rb'\$2\$[\.\/A-Za-z0-9]+\$[\.\/A-Za-z0-9]+', data)
    if bcrypt_matches:
        print(f"Found {len(bcrypt_matches)} bcrypt hashes:")
        for m in bcrypt_matches[:10]:
            print(m.decode('utf-8', errors='replace'))
    else:
        print("No bcrypt hashes found in firmware.")