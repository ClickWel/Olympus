"""
Focused tool calling test for Ministral 14B Reasoning.
Tries multiple strategies that reasoning models respond better to.
"""

import json
import urllib.request

BASE_URL = "http://localhost:1234/v1"
MODEL = "mistralai/ministral-3-14b-reasoning"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from disk",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            }
        }
    }
]

def post(data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())

def run(label, messages, tool_choice="auto"):
    print(f"\n  [{label}]")
    resp = post({
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": tool_choice,
        "max_tokens": 200,
        "temperature": 0
    })
    choice = resp["choices"][0]
    msg = choice["message"]
    tool_calls = msg.get("tool_calls")
    finish = choice.get("finish_reason")

    if tool_calls:
        tc = tool_calls[0]
        print(f"  PASS - called {tc['function']['name']}({tc['function']['arguments']})")
        return True
    else:
        print(f"  FAIL - finish={finish}")
        content = msg.get("content", "")
        if content:
            print(f"  Said: {content[:200]!r}")
        return False

print(f"=== Ministral 14B Tool Calling Test ===")
print(f"Model: {MODEL}\n")

results = []

# Strategy 1: auto, simple prompt
results.append(run(
    "auto / simple",
    [{"role": "user", "content": "Search the web for the latest news about AI."}],
    tool_choice="auto"
))

# Strategy 2: required, forces a call
results.append(run(
    "tool_choice=required",
    [{"role": "user", "content": "Search the web for the latest news about AI."}],
    tool_choice="required"
))

# Strategy 3: system prompt nudge + auto
results.append(run(
    "system nudge + auto",
    [
        {"role": "system", "content": "You are a helpful assistant. When the user asks you to do something, use the available tools to do it. Do not explain - just call the tool."},
        {"role": "user", "content": "Search the web for the latest news about AI."}
    ],
    tool_choice="auto"
))

# Strategy 4: explicit instruction in user message
results.append(run(
    "explicit instruction",
    [
        {"role": "system", "content": "You have access to tools. Use them."},
        {"role": "user", "content": "Use the search_web tool to find: latest AI news"}
    ],
    tool_choice="auto"
))

# Strategy 5: required + explicit
results.append(run(
    "required + explicit",
    [
        {"role": "system", "content": "You have access to tools. Use them."},
        {"role": "user", "content": "Use the search_web tool to find: latest AI news"}
    ],
    tool_choice="required"
))

print(f"\n=== Results ===")
labels = ["auto/simple", "required", "system nudge", "explicit", "required+explicit"]
for label, result in zip(labels, results):
    print(f"  {label:<25} {'PASS' if result else 'FAIL'}")

passed = sum(results)
print(f"\n  {passed}/{len(results)} strategies passed")
if passed > 0:
    print("  Ministral CAN do tool calling - Hermes just needs the right setup.")
else:
    print("  Ministral is not calling tools under any strategy tested.")
    print("  Stick with gemma-3-12b or qwen3.5-9b for Hermes.")
