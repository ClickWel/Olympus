"""
Test LM Studio local server for Hermes integration.
Checks: server reachable, models available, tool calling works.
Tests all loaded models and prints config snippets for each.
"""

import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:1234/v1"

# Models to prefer testing first (partial match ok). Others tested after.
PREFERRED_ORDER = [
    "gemma",   # Gemma 4 31B first
    "qwen",    # Qwen3.5 35B second
]

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def post(path, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())

def get_models():
    resp = get("/models")
    models = [m["id"] for m in resp.get("data", [])]
    # Sort by preferred order
    def sort_key(mid):
        low = mid.lower()
        for i, pref in enumerate(PREFERRED_ORDER):
            if pref in low:
                return i
        return len(PREFERRED_ORDER)
    return sorted(models, key=sort_key)

def test_chat(model_id):
    resp = post("/chat/completions", {
        "model": model_id,
        "messages": [{"role": "user", "content": "Say the word READY and nothing else."}],
        "max_tokens": 10,
        "temperature": 0
    })
    return resp["choices"][0]["message"]["content"].strip()

def test_tool_calling(model_id):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name"}
                    },
                    "required": ["city"]
                }
            }
        }
    ]
    resp = post("/chat/completions", {
        "model": model_id,
        "messages": [{"role": "user", "content": "What is the weather in London?"}],
        "tools": tools,
        "tool_choice": "auto",
        "max_tokens": 100,
        "temperature": 0
    })
    choice = resp["choices"][0]
    msg = choice.get("message", {})
    tool_calls = msg.get("tool_calls")
    if tool_calls:
        tc = tool_calls[0]
        return True, tc["function"]["name"], tc["function"]["arguments"]
    return False, None, msg.get("content", "")

def config_snippet(model_id):
    return f"""\
  # --- Local: {model_id} ---
  - base_url: http://localhost:1234/v1
    api_key: lm-studio
    models:
      {model_id}:
        context_length: 32768

# To activate this model:
#   model:
#     default: {model_id}
#     provider: lm-studio
#     base_url: http://localhost:1234/v1
#     api_mode: chat_completions"""

def run_tests(model_id):
    print(f"\n{'='*60}")
    print(f"  MODEL: {model_id}")
    print(f"{'='*60}")

    # Chat test
    print("  [chat]  ", end="", flush=True)
    try:
        reply = test_chat(model_id)
        print(f"OK  -> {reply!r}")
        chat_ok = True
    except Exception as e:
        print(f"FAIL -> {e}")
        chat_ok = False

    # Tool calling test
    print("  [tools] ", end="", flush=True)
    try:
        ok, fn, args = test_tool_calling(model_id)
        if ok:
            print(f"OK  -> called {fn}({args})")
        else:
            print(f"FAIL -> no tool call. Model said: {args!r}")
        tool_ok = ok
    except Exception as e:
        print(f"FAIL -> {e}")
        tool_ok = False

    return chat_ok, tool_ok

if __name__ == "__main__":
    print("=== LM Studio Integration Test ===")
    print(f"Server: {BASE_URL}\n")

    try:
        model_ids = get_models()
    except urllib.error.URLError as e:
        print(f"ERROR: Cannot reach LM Studio at {BASE_URL}")
        print("  Make sure LM Studio is open and the local server is started.")
        print(f"  Details: {e}")
        raise SystemExit(1)

    if not model_ids:
        print("ERROR: No models returned. Load a model in LM Studio first.")
        raise SystemExit(1)

    print(f"Found {len(model_ids)} model(s): {', '.join(model_ids)}")

    results = {}
    for mid in model_ids:
        chat_ok, tool_ok = run_tests(mid)
        results[mid] = (chat_ok, tool_ok)

    # Summary table
    print(f"\n{'='*60}")
    print("  RESULTS")
    print(f"{'='*60}")
    print(f"  {'Model':<45} {'Chat':<6} {'Tools'}")
    print(f"  {'-'*45} {'-'*5} {'-'*5}")
    for mid, (c, t) in results.items():
        print(f"  {mid:<45} {'OK' if c else 'FAIL':<6} {'OK' if t else 'FAIL'}")

    # Config snippets for passing models
    passing = [mid for mid, (c, t) in results.items() if c and t]
    partial = [mid for mid, (c, t) in results.items() if c and not t]

    print(f"\n{'='*60}")
    print("  CONFIG SNIPPETS (paste into config.yaml > custom_providers)")
    print(f"{'='*60}")

    if passing:
        print("\n  -- Full support (chat + tools) --\n")
        for mid in passing:
            print(config_snippet(mid))
            print()

    if partial:
        print("\n  -- Chat only (no tool calling) --\n")
        for mid in partial:
            print(config_snippet(mid))
            print()

    if not passing and not partial:
        print("\n  No models passed. Check that LM Studio server is running with a model loaded.")

    print(f"\n  NOTE: Only one model can be loaded in LM Studio at a time.")
    print(f"  Load each model separately and re-run this script to test all.")
