import zlib, re, os

def decompress_pdf(path):
    with open(path, 'rb') as f:
        data = f.read()

    # Find all FlateDecode streams
    streams = re.findall(b'stream\r?\n(.*?)\r?\nendstream', data, re.DOTALL)
    print(f"Found {len(streams)} streams")

    for i, stream in enumerate(streams):
        try:
            decompressed = zlib.decompress(stream)
            print(f"\n=== Stream {i} (decompressed {len(decompressed)} bytes) ===")
            print(decompressed[:500])
            # Search for flag
            flag_match = re.search(b'HTB\{[^}]+\}', decompressed)
            if flag_match:
                print(f"\n*** FLAG FOUND: {flag_match.group(0).decode('utf-8', errors='ignore')} ***")
                return flag_match.group(0).decode('utf-8', errors='ignore')
        except Exception as e:
            # Try raw deflate
            try:
                decompressed = zlib.decompress(stream, -15)
                print(f"\n=== Stream {i} raw deflate (decompressed {len(decompressed)} bytes) ===")
                print(decompressed[:500])
                flag_match = re.search(b'HTB\{[^}]+\}', decompressed)
                if flag_match:
                    print(f"\n*** FLAG FOUND: {flag_match.group(0).decode('utf-8', errors='ignore')} ***")
                    return flag_match.group(0).decode('utf-8', errors='ignore')
            except:
                print(f"Stream {i}: decompression failed ({e})")
    return None

flag = decompress_pdf('D:/Olympus/ctf/output/phreaks_plan.pdf')
if flag:
    print(f"\nFLAG: {flag}")
else:
    print("\nNo flag found in PDF streams")
