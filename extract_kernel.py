import struct, zlib, lzma

firmware_path = r"C:\Users\click\Desktop\forensics_silicon_data_sleuthing (1)\chal_router_dump.bin"

with open(firmware_path, "rb") as f:
    # uImage header at 0x180000 (64 bytes)
    f.seek(0x180000)
    uimage_header = f.read(64)
    # Unpack 64-byte uImage header
    magic, hcrc, time, size, load, ep, dcrc = struct.unpack('>IIIIIII', uimage_header[:28])
    os, arch, img_type, comp = struct.unpack('BBBB', uimage_header[28:32])
    name = uimage_header[32:64]
    name_str = name.rstrip(b'\x00').decode('utf-8', errors='replace')

    print(f"uImage magic: 0x{magic:x} (expected 0x27051956)")
    print(f"Data size: {size} bytes")
    print(f"Compression: {comp} (1=gzip, 2=bzip2, 3=lzma, 4=lzo)")
    print(f"Name: {name_str}")

    # Read kernel data (after 64-byte header)
    kernel_data = f.read(size)
    print(f"Read {len(kernel_data)} bytes of kernel data")

    # Decompress kernel
    decompressed = None
    if comp == 1: # gzip
        print("Decompressing gzip...")
        try:
            decompressed = zlib.decompress(kernel_data, 15 + 32)
        except Exception as e:
            print(f"Gzip error: {e}")
    elif comp == 3: # lzma
        print("Decompressing lzma...")
        try:
            decompressed = lzma.decompress(kernel_data)
        except Exception as e:
            print(f"LZMA error: {e}")
    else:
        print(f"Unsupported compression: {comp}")
        decompressed = kernel_data

    if decompressed:
        print(f"Decompressed kernel size: {len(decompressed)} bytes")
        # Search for interesting strings
        import re
        strings = re.findall(b'[\x20-\x7e]{6,}', decompressed)
        for s in strings:
            s_str = s.decode('utf-8', errors='replace')
            if any(k in s_str.lower() for k in ['root:', 'password', 'shadow', 'login', 'init=', 'root=']):
                print(f"Kernel string: {s_str}")