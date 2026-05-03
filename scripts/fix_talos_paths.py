path = '/home/click/.hermes/profiles/talos/SOUL.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('D:\\Talos\\memory\\MEMORY.md', '/mnt/d/Talos/memory/MEMORY.md'),
    ('D:\\Talos\\sessions', '/mnt/d/Talos/sessions'),
    ('D:\\Shared\\copy_output.txt', '/mnt/d/Shared/copy_output.txt'),
    ('D:\\Shared\\', '/mnt/d/Shared/'),
    ('D:\\Shared', '/mnt/d/Shared'),
    ('D:\\Hermes', '/mnt/d/Hermes'),
    ('D:\\Ares', '/mnt/d/Ares'),
]
for old, new in replacements:
    content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
