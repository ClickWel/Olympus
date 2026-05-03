fixes = [
    (
        '/home/click/.hermes/profiles/talos/SOUL.md',
        [('D:\\Talos sessions', '/mnt/d/Talos/sessions')]
    ),
    (
        '/home/click/.hermes/profiles/ares/SOUL.md',
        [
            ('D:\\Ares\\sessions\\YYYY-MM-DD.md', '/mnt/d/Ares/sessions/YYYY-MM-DD.md'),
            ('D:\\Shared\\mission_state.md', '/mnt/d/Shared/mission_state.md'),
        ]
    ),
]

for path, replacements in fixes:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Done: {path}')
