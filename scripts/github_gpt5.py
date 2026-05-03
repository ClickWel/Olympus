#!/usr/bin/env python3
"""Quick GPT-5 test via GitHub Models API using OpenAI client."""
import os, sys

# Load token from env file
token = None
env_path = "D:/Hermes/config/MASTER_API_KEYS.env"
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GITHUB_MODELS_API_KEY="):
                token = line.strip().split("=", 1)[1]
                break

if not token:
    token = os.environ.get("GITHUB_MODELS_API_KEY")

if not token:
    print("No GitHub Models API key found.")
    sys.exit(1)

from openai import OpenAI

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=token,
)

print("Sending request to openai/gpt-5...")
try:
    response = client.chat.completions.create(
        model="openai/gpt-5",
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
        extra_headers={"X-GitHub-Api-Version": "2026-03-10"},
        timeout=30,
    )
    print(f"\nResponse:\n{response.choices[0].message.content}\n")
    print(f"Model used: {response.model}")
except Exception as e:
    print(f"Error: {e}")
