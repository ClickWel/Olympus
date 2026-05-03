import urllib.request
import json

url = "http://10.0.0.25:1234/v1/chat/completions"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"]
            }
        }
    }
]

payload = {
    "model": "qwen3.5-9b-glm5.1-distill-v1",
    "messages": [
        {"role": "user", "content": "What is the weather in Dublin?"}
    ],
    "tools": tools,
    "tool_choice": "auto",
    "temperature": 0.4,
    "max_tokens": 256
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

with urllib.request.urlopen(req, timeout=30) as resp:
    result = json.loads(resp.read().decode("utf-8"))

msg = result["choices"][0]["message"]
print("Finish reason:", result["choices"][0]["finish_reason"])

if msg.get("tool_calls"):
    tc = msg["tool_calls"][0]
    print("PASS - tool call fired:")
    print("  Function:", tc["function"]["name"])
    print("  Args:", tc["function"]["arguments"])
else:
    print("FAIL - no tool call. Raw content:")
    print(msg.get("content", "(empty)"))
