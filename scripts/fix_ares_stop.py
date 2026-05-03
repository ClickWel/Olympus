path = '/home/click/.hermes/profiles/ares/SOUL.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'When Jeff or Hermes says "stop", "abort", "wait", or signals to halt - HARD STOP IMMEDIATELY. Do not finish the current operation. Then confirm: "Stopped. What\'s next?"'
new = 'When Jeff or Hermes says "stop", "abort", "wait", or signals to halt - HARD STOP IMMEDIATELY. Do not finish the current operation. Output exactly: "Stopped." Do not resume unless Jeff explicitly says to continue.'

content = content.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
