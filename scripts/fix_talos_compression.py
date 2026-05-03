path = '/home/click/.hermes/profiles/talos/config.yaml'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'compression:\n  enabled: true\n  protect_last_n: 30\n  summary_base_url: null\n  summary_model: google/gemini-3-flash-preview\n  summary_provider: auto\n  target_ratio: 0.25\n  threshold: 0.65',
    'compression:\n  enabled: true\n  protect_last_n: 30\n  summary_base_url: null\n  summary_model: openrouter/auto\n  summary_provider: openrouter\n  target_ratio: 0.25\n  threshold: 0.65'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
