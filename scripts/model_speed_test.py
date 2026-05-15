import urllib.request
import urllib.error
import json
import time
import os

API_KEY = "***REMOVED***"
MODELS = [
    "poolside/laguna-m.1:free",
    "z-ai/glm-4.5-air:free",
]
PROMPT = "Explain the difference between TCP and UDP in exactly 200 words."

def test_model(model):
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            elapsed = time.time() - start
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  ERROR {e.code}: {e.read().decode()}")
        return
    except Exception as e:
        print(f"  ERROR: {e}")
        return

    usage = data.get("usage", {})
    completion_tokens = usage.get("completion_tokens", 0)
    tps = completion_tokens / elapsed if elapsed > 0 else 0

    print(f"  Time:       {elapsed:.2f}s")
    print(f"  Tokens out: {completion_tokens}")
    print(f"  Speed:      {tps:.1f} tok/s")
    print(f"  Response:   {data['choices'][0]['message']['content'][:80]}...")

for model in MODELS:
    print(f"\n{model}")
    print("-" * len(model))
    test_model(model)
