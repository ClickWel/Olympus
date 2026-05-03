path = '/home/click/.hermes/profiles/talos/config.yaml'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('  protect_last_n: 30', '  protect_last_n: 50')
content = content.replace('  target_ratio: 0.25', '  target_ratio: 0.4')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
