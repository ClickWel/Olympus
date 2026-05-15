import os, json

base_dirs = ['D:\\', 'C:\\Users\\click\\']
for base in base_dirs:
    for root, dirs, files in os.walk(base):
        depth = root.replace(base, '').count(os.sep)
        if depth > 4:
            dirs.clear()
            continue
        if 'settings.json' in files and '.claude' in root:
            p = os.path.join(root, 'settings.json')
            try:
                with open(p, encoding='utf-8') as f:
                    d = json.load(f)
                mcp = d.get('mcpServers', {})
                notion_keys = [k for k in mcp if 'notion' in k.lower()]
                if notion_keys:
                    print('FOUND in ' + p + ': ' + str(notion_keys))
                else:
                    print('Clean: ' + p)
            except Exception as e:
                print('Error ' + p + ': ' + str(e))
