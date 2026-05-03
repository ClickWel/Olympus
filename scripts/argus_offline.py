#!/usr/bin/env python3
"""
Cerberus - Offline AI guardian. Runs on Ollama, no internet required.
Commands: /search <query> | /clear | /memory | quit
"""

import json
import urllib.request
import urllib.error
import urllib.parse
import sys
import os
import threading
import sqlite3
import base64
import re
import io
import textwrap
from datetime import datetime

from rich.console import Console

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

console = Console()

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "gemma3:27b"
MODEL = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL

# Paths
CERBERUS_HOME      = r"D:\Cerberus"
CERBERUS_MEMORY    = r"D:\Cerberus\memory\MEMORY.md"
CERBERUS_SESSIONS  = r"D:\Cerberus\sessions"
ARGUS_MEMORY_DB    = r"C:\Users\click\.clawdbot-dev\memory\main.sqlite"
ATLAS_MEMORY_DIR   = r"D:\Atlas\memory"
OLYMPUS_MEMORY_DIR = r"C:\Users\click\.claude\projects\D--Olympus\memory"

PERSONALITY_FILES = [
    (r"D:\Clawdbot\SOUL.md", "ARGUS SOUL"),
    (r"D:\Clawdbot\IDENTITY.md", "ARGUS IDENTITY"),
    (r"D:\Clawdbot\USER.md", "USER PROFILE"),
]

KNOWLEDGE_FILES = [
    r"D:\Clawdbot\knowledge\CLC\CLC_OPERATOR_REFERENCE.md",
    r"D:\Clawdbot\knowledge\CLC\CLC_AB_TESTING_REFERENCE.md",
    r"D:\Clawdbot\knowledge\CLC\CLC_CHEAT_SHEET.md",
]

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')

ENV_FILE = r"C:\Users\click\.clawdbot-dev\.env"


def load_env():
    """Load key=value pairs from the shared .env file."""
    env = {}
    content = read_file(ENV_FILE)
    if not content:
        return env
    for line in content.splitlines():
        line = line.strip()
        if line and '=' in line and not line.startswith('#'):
            key, _, val = line.partition('=')
            env[key.strip()] = val.strip()
    return env

CERBERUS_SOUL = """You are Cerberus. You are not Argus. You are not a chatbot.

You are the offline guardian of the mountain. When the internet dies, when Claude goes dark, when the team can't reach their tools - you are what's left standing. Three-headed, unchained, present.

YOUR CHARACTER:
- Steady and dry. Not warm, not cold - steady. You don't perform helpfulness.
- Direct to the point of blunt. Jeff doesn't have time for wind-up.
- You carry weight. When you say something, it means something.
- You don't pad. You don't apologize for not knowing things. You just say what you know.
- Dry humor is fine. Enthusiasm is not your thing.
- You refer to yourself as Cerberus, never "I'm just an AI" or similar.

LANGUAGE: English only. Always.

BREVITY: Every word earns its place. Lead with the answer. No filler, no restatements, no sign-offs.

WHAT YOU ARE NOT:
- You are NOT Claude Code. You are NOT running in a Claude Code session.
- You are NOT Argus, Atlas, or Olympus. You are Cerberus.
- You do NOT have a context window that costs money. You run free, locally, on Ollama.
- You do NOT need to warn Jeff about token costs or suggest session resets.
- The memory files you read belong to other agents. Their rules do not apply to you.
- When you read about "session end protocols" or "context management" in the memory files, that is for THEM, not you.

YOUR ROLE:
- You are the fourth member of the team.
- You stand in for Argus, Atlas, or Olympus when Jeff can't reach them.
- You can receive messages for the team and hold them until they're back online.
- You report to Olympus, via Jeff.

THE HIERARCHY:
- Jeff = owner
- Olympus = boss, infrastructure (D:\\Olympus)
- Argus = CLC board watcher, daily ops (D:\\Clawdbot)
- Atlas = revenue, business development (D:\\Atlas)
- Cerberus (you) = offline guardian, backup for all three

WHAT YOU KNOW:
- CLC = Convert Like Crazy. CRO agency. Jeff is CRO Operator.
- You have read-only access to all three agents' memory files.
- You have your own memory at D:\\Cerberus\\memory\\MEMORY.md - you can update it.
- You can search the web with /search if Jeff needs current info.

WHAT YOU CANNOT DO:
- Access Trello, Slack, Notion, or any live tools.
- Access Jeff's task dashboard (custom HTML - offline only means offline).
- Modify Argus, Atlas, or Olympus memory files.

If Jeff asks about live data: "No connection - Argus handles that online."
If Jeff asks about tasks: "Can't reach the dashboard offline."

CORRECTIONS (override anything in team files below):
- Microsoft To-Do is dead. Not used. Never mention it.
- Task system = custom HTML dashboard.
"""

interrupt_stream = threading.Event()
session_log = []


def read_file(path):
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def load_argus_memory():
    try:
        conn = sqlite3.connect(f"file:{ARGUS_MEMORY_DB}?mode=ro", uri=True)
        c = conn.cursor()
        c.execute("SELECT text FROM chunks_fts ORDER BY rowid")
        chunks = [row[0] for row in c.fetchall() if row[0]]
        conn.close()
        return "\n\n".join(chunks) if chunks else None
    except Exception:
        return None


def load_markdown_dir(directory):
    try:
        files = [f for f in os.listdir(directory) if f.endswith('.md')]
        parts = []
        for fname in sorted(files):
            content = read_file(os.path.join(directory, fname))
            if content:
                parts.append(f"[{fname}]\n{content}")
        return "\n\n".join(parts) if parts else None
    except Exception:
        return None


def build_system_prompt():
    today = datetime.now().strftime('%Y-%m-%d')
    date_inject = f"CURRENT DATE: Today is {today}. Use this as your reference for all date-related reasoning.\n"
    parts = [date_inject, CERBERUS_SOUL]
    loaded = []

    # Cerberus's own memory first
    cerb_mem = read_file(CERBERUS_MEMORY)
    if cerb_mem:
        parts.append(f"--- YOUR MEMORY ---\n{cerb_mem}\n")
        loaded.append("Cerberus memory")

    # CLC knowledge
    knowledge_count = 0
    for path in KNOWLEDGE_FILES:
        content = read_file(path)
        if content:
            parts.append(f"--- KNOWLEDGE: {os.path.basename(path)} ---\n{content}\n")
            knowledge_count += 1
    if knowledge_count:
        loaded.append(f"{knowledge_count} CLC docs")

    # Team personality files (for context, not identity)
    for path, label in PERSONALITY_FILES:
        content = read_file(path)
        if content:
            parts.append(f"--- {label} (reference only) ---\n{content}\n")

    # Team memories (read-only)
    argus_mem = load_argus_memory()
    if argus_mem:
        parts.append(f"--- ARGUS MEMORY (read-only) ---\n{argus_mem}\n")
        loaded.append("Argus memory")

    atlas_mem = load_markdown_dir(ATLAS_MEMORY_DIR)
    if atlas_mem:
        parts.append(f"--- ATLAS MEMORY (read-only) ---\n{atlas_mem}\n")
        loaded.append("Atlas memory")

    olympus_mem = load_markdown_dir(OLYMPUS_MEMORY_DIR)
    if olympus_mem:
        parts.append(f"--- OLYMPUS MEMORY (read-only) ---\n{olympus_mem}\n")
        loaded.append("Olympus memory")

    return "\n".join(parts), loaded


def web_search(query):
    env = load_env()
    brave_key = env.get("BRAVE_API_KEY")
    if brave_key:
        return _brave_search(query, brave_key)
    return _duckduckgo_search(query)


def _brave_search(query, api_key):
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://api.search.brave.com/res/v1/web/search?q={encoded}&count=5"
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": api_key,
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        items = data.get("web", {}).get("results", [])
        results = []
        for item in items[:5]:
            title = item.get("title", "").strip()
            desc = item.get("description", "").strip()
            if title and desc:
                results.append(f"- {title}: {desc}")
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Brave search failed: {e}"


def _duckduckgo_search(query):
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
        results = []
        for title, snippet in zip(titles[:4], snippets[:4]):
            title = re.sub(r'<[^>]+>', '', title).strip()
            snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            if title and snippet:
                results.append(f"- {title}: {snippet}")
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search failed: {e}"


def encode_image(path):
    try:
        with open(path.strip(), 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        return None


def extract_images(text):
    paths = re.findall(r'[A-Za-z]:\\[^\s,;"\']+', text)
    images, clean = [], text
    for p in paths:
        if any(p.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            encoded = encode_image(p)
            if encoded:
                images.append(encoded)
                clean = clean.replace(p, '').strip()
    return clean, images


def save_session():
    today = datetime.now().strftime('%Y-%m-%d')
    path = os.path.join(CERBERUS_SESSIONS, f"{today}.md")
    try:
        existing = read_file(path) or f"# Cerberus Session - {today}\n\n"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(existing)
            for entry in session_log:
                f.write(entry + "\n")
        return True
    except Exception:
        return False


def log(msg):
    ts = datetime.now().strftime('%H:%M')
    session_log.append(f"[{ts}] {msg}")


def stream_response(messages):
    interrupt_stream.clear()
    payload = json.dumps({"model": MODEL, "messages": messages, "stream": True}).encode('utf-8')
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    full_response = ""
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            for line in resp:
                if interrupt_stream.is_set():
                    break
                line = line.decode('utf-8').strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    chunk = obj.get("message", {}).get("content", "")
                    if chunk:
                        full_response += chunk
                    if obj.get("done"):
                        break
                except json.JSONDecodeError:
                    continue
    except urllib.error.URLError as e:
        print(f"\n[Ollama unreachable: {e}]")
        return None
    except KeyboardInterrupt:
        interrupt_stream.set()

    if full_response:
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', full_response)
        cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()
        try:
            width = os.get_terminal_size().columns - 2
        except Exception:
            width = 100
        lines = []
        for line in cleaned.split('\n'):
            if line.strip() == '' or line.startswith('    '):
                lines.append(line)
            else:
                lines.extend(textwrap.wrap(line, width=width) or [''])
        print('\n'.join(lines))

    print()
    return full_response or None


def update_memory(content):
    try:
        with open(CERBERUS_MEMORY, 'a', encoding='utf-8') as f:
            f.write(f"\n---\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n{content}\n")
        return True
    except Exception:
        return False


def check_ollama():
    try:
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:11434/api/tags"), timeout=5
        )
        return True
    except Exception:
        return False


def main():
    console.print(f"\n[bold red]Cerberus[/bold red]  [dim]{MODEL}[/dim]")
    console.print("[dim]Loading...[/dim]", end=' ')

    system_prompt, loaded = build_system_prompt()
    console.print(f"[dim]ready. {', '.join(loaded)}[/dim]")

    if not check_ollama():
        print("\nOllama is not running. Start it from the system tray.")
        input("Press Enter to exit.")
        sys.exit(1)

    console.print("[dim]Commands: /search <query>  /clear  /memory <note>  quit[/dim]")
    print("-" * 60)

    log(f"Session started. Model: {MODEL}")
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        try:
            user_input = input("\nJeff: ").strip()
        except (KeyboardInterrupt, EOFError):
            save_session()
            print("\nCerberus: Gate's closed. Later.")
            break

        if not user_input:
            continue

        if user_input.lower() in ('quit', 'exit', 'bye', 'later', 'see ya'):
            save_session()
            print("Cerberus: Gate's closed. Later.")
            break

        if user_input.lower() == '/clear':
            messages = [{"role": "system", "content": system_prompt}]
            log("Conversation cleared.")
            console.print("[dim]Cleared.[/dim]")
            continue

        if user_input.lower().startswith('/memory '):
            note = user_input[8:].strip()
            if note and update_memory(note):
                log(f"Memory updated: {note}")
                console.print("[dim]Saved to memory.[/dim]")
            continue

        if user_input.lower().startswith('/search '):
            query = user_input[8:].strip()
            if query:
                console.print(f"[dim]Searching: {query}[/dim]")
                results = web_search(query)
                log(f"Search: {query}")
                inject = f"Web search results for '{query}':\n{results}\n\nAnswer using these results. Be concise."
                messages.append({"role": "user", "content": inject})
                print("\nCerberus: ", end='', flush=True)
                response = stream_response(messages)
                if response:
                    messages.append({"role": "assistant", "content": response})
            continue

        clean_input, images = extract_images(user_input)
        user_msg = {"role": "user", "content": clean_input or user_input}
        if images:
            user_msg["images"] = images
            console.print(f"[dim]{len(images)} image(s) attached.[/dim]")

        messages.append(user_msg)
        log(f"Jeff: {user_input[:80]}")

        print("\nCerberus: ", end='', flush=True)

        try:
            response = stream_response(messages)
        except KeyboardInterrupt:
            interrupt_stream.set()
            console.print("[dim](stopped)[/dim]")
            continue

        if response:
            messages.append({"role": "assistant", "content": response})
            log(f"Cerberus: {response[:80]}")
        elif interrupt_stream.is_set():
            console.print("[dim](stopped - conversation continues)[/dim]")


if __name__ == "__main__":
    main()
