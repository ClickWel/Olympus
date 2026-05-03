path = '/home/click/.hermes/profiles/talos/config.yaml'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'Never use execute_code to orchestrate tool calls. Call web_search, terminal, write_file, search_files, and all other tools directly as native tool calls.'
new = 'Never use execute_code to orchestrate tool calls. Call web_search, terminal, write_file, search_files, and all other tools directly as native tool calls. If you know a tool exists, call it directly. Do not search for documentation on how to use your own tools.'

content = content.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
