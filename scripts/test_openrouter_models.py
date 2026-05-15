import json, os, urllib.request, urllib.error

# Read OpenRouter API key
with open(r'D:\Shared\MASTER_API_KEYS.env', 'r') as f:
    for line in f:
        if line.startswith('OPENROUTER_API_KEY='):
            api_key = line.strip().split('=', 1)[1]
            break

# Models to test (free + vision)
models = [
    'nvidia/nemotron-nano-12b-v2-vl:free',
    'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free',
    'google/gemma-4-26b-a4b-it:free',
    'google/gemma-3-12b-it:free',
    'google/gemma-3-4b-it:free',
]

url = "https://openrouter.ai/api/v1/messages"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://localhost",
    "X-Title": "Olympus Test"
}

for model in models:
    payload = json.dumps({
        "model": model,
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "hi"}]
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"OK: {model}")
    except urllib.error.HTTPError as e:
        print(f"FAIL ({e.code}): {model} - {e.read().decode()[:100]}")
    except Exception as e:
        print(f"ERROR: {model} - {e}")
