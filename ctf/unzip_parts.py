import zipfile, os

attach_dir = 'D:/Olympus/ctf/attachments'
passwords = {}
with open(os.path.join(attach_dir, 'passwords.txt')) as f:
    for line in f:
        if ':' in line:
            fname, pw = line.strip().split(': ')
            passwords[fname] = pw

for fname, pw in passwords.items():
    zip_path = os.path.join(attach_dir, fname)
    extract_dir = os.path.join(attach_dir, fname.replace('.zip', ''))
    os.makedirs(extract_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extract_dir, pwd=pw.encode())
            print(f"Extracted {fname} to {extract_dir}")
            # List extracted files
            for f in os.listdir(extract_dir):
                print(f"  - {f}")
    except Exception as e:
        print(f"Failed to extract {fname}: {e}")
