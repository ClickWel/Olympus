path = '/home/click/.hermes/profiles/ares/config.yaml'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('NOTION_TOKEN: PASTE_TOKEN_HERE', 'NOTION_TOKEN: ${NOTION_TOKEN}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
