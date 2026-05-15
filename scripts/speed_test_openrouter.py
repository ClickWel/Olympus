import json, time, urllib.request, urllib.error

with open(r'D:\Olympus\MASTER_API_KEYS.env', 'r') as f:
    for line in f:
        if line.startswith('OPENROUTER_API_KEY='):
            api_key = line.strip().split('=', 1)[1]
            break

models = [
    'google/gemma-3-12b-it:free',
    'google/gemma-3-4b-it:free',
    'nvidia/nemotron-nano-12b-v2-vl:free',
]

url = "https://openrouter.ai/api/v1/messages"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://localhost",
    "X-Title": "Olympus Speed Test"
}

for model in models:
    payload = json.dumps({
        "model": model,
        "max_tokens": 50,
        "messages": [{"role": "user", "content": "Say hello in 5 words"}]
    }).encode('utf-8')

    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        start = time.time()
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed = time.time() - start
            data = json.loads(resp.read())
            print(f"{model}: {elapsed:.2f}s")
    except Exception as e:
        print(f"{model}: FAILED - {e}")
