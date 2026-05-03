path = '/home/click/.hermes/profiles/talos/SOUL.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('/mnt/d/Talos/sessions\\', '/mnt/d/Talos/sessions/')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
