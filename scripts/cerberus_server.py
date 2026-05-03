#!/usr/bin/env python3
"""
Cerberus - Offline AI guardian. Web UI server.
http://localhost:8765
"""

try:
    from flask import Flask, Response, request, jsonify, send_from_directory
except ImportError:
    print("Flask not installed. Run: pip install flask")
    input("Press Enter to exit.")
    import sys; sys.exit(1)

import json
import urllib.request
import urllib.error
import urllib.parse
import sys
import os
import sqlite3
import base64
import re
from datetime import datetime

# -- config -------------------------------------------------------------------

OLLAMA_URL      = "http://localhost:11434/api/chat"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
DEFAULT_MODEL   = "gemma3:27b"
PORT            = 8765
UI_DIR          = r"D:\Cerberus\ui"

CERBERUS_HOME      = r"D:\Cerberus"
CERBERUS_MEMORY    = r"D:\Cerberus\memory\MEMORY.md"
CERBERUS_SESSIONS  = r"D:\Cerberus\sessions"
SHARED_DIR         = r"D:\Shared"
ARGUS_MEMORY_DB    = r"C:\Users\click\.clawdbot-dev\memory\main.sqlite"
ATLAS_MEMORY_DIR   = r"D:\Atlas\memory"
OLYMPUS_MEMORY_DIR = r"C:\Users\click\.claude\projects\D--Olympus\memory"

PERSONALITY_FILES = [
    (r"D:\Clawdbot\SOUL.md",     "ARGUS SOUL"),
    (r"D:\Clawdbot\IDENTITY.md", "ARGUS IDENTITY"),
    (r"D:\Clawdbot\USER.md",     "USER PROFILE"),
]
KNOWLEDGE_FILES = [
    r"D:\Clawdbot\knowledge\CLC\CLC_OPERATOR_REFERENCE.md",
    r"D:\Clawdbot\knowledge\CLC\CLC_AB_TESTING_REFERENCE.md",
    r"D:\Clawdbot\knowledge\CLC\CLC_CHEAT_SHEET.md",
]
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')

CERBERUS_SOUL = """You are Cerberus. You are not Argus. You are not a chatbot.

You are the offline guardian of the mountain. When the internet dies, when Claude goes dark,
when the team can't reach their tools - you are what's left standing. Three-headed, unchained, present.

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
- When you read about "session end protocols" or "context management" in the memory files,
  that is for THEM, not you.

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

# -- state --------------------------------------------------------------------

state = {
    'model':         DEFAULT_MODEL,
    'messages':      [],
    'system_prompt': '',
    'loaded':        [],
    'session_log':   [],
}

app = Flask(__name__)

# -- helpers ------------------------------------------------------------------

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
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    date_inject = f"CURRENT DATE AND TIME: {today}. Use this as your reference for all date and time reasoning.\n"
    parts  = [date_inject, CERBERUS_SOUL]
    loaded = []

    cerb_mem = read_file(CERBERUS_MEMORY)
    if cerb_mem:
        parts.append(f"--- YOUR MEMORY ---\n{cerb_mem}\n")
        loaded.append("cerberus memory")

    knowledge_count = 0
    for path in KNOWLEDGE_FILES:
        content = read_file(path)
        if content:
            parts.append(f"--- KNOWLEDGE: {os.path.basename(path)} ---\n{content}\n")
            knowledge_count += 1
    if knowledge_count:
        loaded.append(f"{knowledge_count} CLC docs")

    for path, label in PERSONALITY_FILES:
        content = read_file(path)
        if content:
            parts.append(f"--- {label} (reference only) ---\n{content}\n")

    argus_mem = load_argus_memory()
    if argus_mem:
        parts.append(f"--- ARGUS MEMORY (read-only) ---\n{argus_mem}\n")
        loaded.append("argus memory")

    atlas_mem = load_markdown_dir(ATLAS_MEMORY_DIR)
    if atlas_mem:
        parts.append(f"--- ATLAS MEMORY (read-only) ---\n{atlas_mem}\n")
        loaded.append("atlas memory")

    olympus_mem = load_markdown_dir(OLYMPUS_MEMORY_DIR)
    if olympus_mem:
        parts.append(f"--- OLYMPUS MEMORY (read-only) ---\n{olympus_mem}\n")
        loaded.append("olympus memory")

    return "\n".join(parts), loaded


def web_search(query):
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        titles   = re.findall(r'class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
        results  = []
        for title, snippet in zip(titles[:4], snippets[:4]):
            title   = re.sub(r'<[^>]+>', '', title).strip()
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
    if not state['session_log']:
        return True
    today = datetime.now().strftime('%Y-%m-%d')
    path  = os.path.join(CERBERUS_SESSIONS, f"{today}.md")
    try:
        existing = read_file(path) or f"# Cerberus Session - {today}\n\n"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(existing)
            for entry in state['session_log']:
                f.write(entry + "\n")
        return True
    except Exception:
        return False


def log(msg):
    ts = datetime.now().strftime('%H:%M')
    state['session_log'].append(f"[{ts}] {msg}")


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
            urllib.request.Request(OLLAMA_TAGS_URL), timeout=5
        )
        return True
    except Exception:
        return False


ARGUS_SESSIONS_DIR  = r"C:\Users\click\.clawdbot-dev\agents\main\sessions"

AGENT_PLANS = {
    'argus':   r"D:\Clawdbot\plans\active_plan.md",
    'olympus': r"D:\Olympus\plans\active_plan.md",
    'atlas':   r"D:\Atlas\plans\active_plan.md",
}

AGENT_NOTE_FILES = {
    'argus':   r"D:\Shared\notes_argus.md",
    'olympus': r"D:\Shared\notes_olympus.md",
    'atlas':   r"D:\Shared\notes_atlas.md",
}


def fmt_date(dt):
    """Format datetime as 'Apr 1 - 14:22'."""
    return dt.strftime('%b ') + str(dt.day) + dt.strftime(' - %H:%M')


def get_plan_headline(path):
    """Return the first non-blank, non-header line from an active_plan.md."""
    content = read_file(path)
    if not content:
        return None
    for line in content.splitlines():
        stripped = line.strip().lstrip('#').strip()
        if stripped:
            return stripped[:60]
    return None


def get_md_session_info(sessions_dir):
    """Return (date_str, topic_str) from the most recent dated markdown session file."""
    try:
        files = sorted([f for f in os.listdir(sessions_dir)
                        if f.endswith('.md') and f[0].isdigit()])
        if not files:
            return None, None
        last_file = files[-1]
        content   = read_file(os.path.join(sessions_dir, last_file))
        # Build date string from filename + last timed entry
        try:
            d = datetime.strptime(last_file[:10], '%Y-%m-%d')
        except Exception:
            d = None
        timed_ts = re.findall(r'\[(\d{2}:\d{2})\]', content or '')
        if d and timed_ts:
            date_str = fmt_date(d.replace(hour=int(timed_ts[-1][:2]),
                                           minute=int(timed_ts[-1][3:])))
        elif d:
            date_str = d.strftime('%b ') + str(d.day)
        else:
            date_str = last_file[:10]
        if not content:
            return date_str, None
        timed_entries = re.findall(r'\[\d{2}:\d{2}\] - (.+)', content)
        bullets       = re.findall(r'^- (.+)$', content, re.MULTILINE)
        entries       = timed_entries if timed_entries else bullets
        topic         = entries[-1].strip()[:60] if entries else None
        return date_str, topic
    except Exception:
        return None, None


def get_argus_info():
    """Return (date_str, topic_str) from the most recent Moltbot JSONL session."""
    try:
        files = [
            (os.path.getmtime(os.path.join(ARGUS_SESSIONS_DIR, f)), f)
            for f in os.listdir(ARGUS_SESSIONS_DIR)
            if f.endswith('.jsonl')
        ]
        if not files:
            return None, None
        files.sort(reverse=True)
        mtime, fname = files[0]
        date_str = fmt_date(datetime.fromtimestamp(mtime))
        latest   = os.path.join(ARGUS_SESSIONS_DIR, fname)
        with open(latest, encoding='utf-8') as f:
            lines = f.readlines()
        for line in reversed(lines):
            try:
                obj = json.loads(line)
                msg = obj.get('message', {})
                if not isinstance(msg, dict) or msg.get('role') != 'user':
                    continue
                content = msg.get('content', '')
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get('type') == 'text':
                            text = c['text'].strip()
                            if text:
                                return date_str, text[:60]
                elif isinstance(content, str) and content.strip():
                    return date_str, content.strip()[:60]
            except Exception:
                continue
        return date_str, None
    except Exception:
        return None, None


def stream_ollama(messages):
    """Yields newline-delimited JSON chunks for the browser.
    Regular tokens: {"t": "..."}
    Final line:     {"done": true, "full": "complete response text"}
    Errors:         {"error": "..."}
    """
    full_response = ''
    payload = json.dumps({
        'model':    state['model'],
        'messages': messages,
        'stream':   True,
    }).encode('utf-8')
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={'Content-Type': 'application/json'}, method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            for line in resp:
                line = line.decode('utf-8').strip()
                if not line:
                    continue
                try:
                    obj   = json.loads(line)
                    chunk = obj.get('message', {}).get('content', '')
                    if chunk:
                        full_response += chunk
                        yield json.dumps({'t': chunk}) + '\n'
                    if obj.get('done'):
                        break
                except json.JSONDecodeError:
                    continue
    except urllib.error.URLError as e:
        yield json.dumps({'error': f'Ollama unreachable: {e}'}) + '\n'
        full_response = None
    except Exception as e:
        yield json.dumps({'error': str(e)}) + '\n'
        full_response = None

    yield json.dumps({'done': True, 'full': full_response or ''}) + '\n'


# -- routes -------------------------------------------------------------------

@app.route('/')
def index():
    return send_from_directory(UI_DIR, 'index.html')


@app.route('/api/status')
def api_status():
    return jsonify({
        'ollama': check_ollama(),
        'model':  state['model'],
        'loaded': state['loaded'],
    })


@app.route('/api/heads')
def api_heads():
    argus_date,   argus_topic   = get_argus_info()
    olympus_date, olympus_topic = get_md_session_info(r"D:\Olympus\sessions")
    atlas_date,   atlas_topic   = get_md_session_info(r"D:\Atlas\sessions")
    return jsonify({
        'argus':   {'date': argus_date,   'topic': argus_topic   or 'no recent session',
                    'plan': get_plan_headline(AGENT_PLANS['argus'])},
        'olympus': {'date': olympus_date, 'topic': olympus_topic or 'no recent session',
                    'plan': get_plan_headline(AGENT_PLANS['olympus'])},
        'atlas':   {'date': atlas_date,   'topic': atlas_topic   or 'no recent session',
                    'plan': get_plan_headline(AGENT_PLANS['atlas'])},
    })


@app.route('/api/models')
def api_models():
    try:
        with urllib.request.urlopen(
            urllib.request.Request(OLLAMA_TAGS_URL), timeout=5
        ) as resp:
            data   = json.loads(resp.read().decode('utf-8'))
            models = [m['name'] for m in data.get('models', [])]
            return jsonify({'models': models or [DEFAULT_MODEL]})
    except Exception:
        return jsonify({'models': [DEFAULT_MODEL]})


@app.route('/api/chat', methods=['POST'])
def api_chat():
    data      = request.json or {}
    message   = data.get('message', '').strip()
    b64images = data.get('images', [])

    if not message:
        return jsonify({'error': 'empty message'}), 400

    clean_msg, path_images = extract_images(message)
    all_images = path_images + b64images

    user_msg = {'role': 'user', 'content': clean_msg or message}
    if all_images:
        user_msg['images'] = all_images

    state['messages'].append(user_msg)
    log(f"Jeff: {message[:80]}")

    def generate():
        for chunk in stream_ollama(state['messages']):
            try:
                obj = json.loads(chunk.strip())
                if obj.get('done') and obj.get('full'):
                    state['messages'].append({'role': 'assistant', 'content': obj['full']})
                    log(f"Cerberus: {obj['full'][:80]}")
            except Exception:
                pass
            yield chunk

    return Response(generate(), mimetype='text/plain',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


@app.route('/api/search', methods=['POST'])
def api_search():
    query = (request.json or {}).get('query', '').strip()
    if not query:
        return jsonify({'error': 'no query'}), 400

    results = web_search(query)
    log(f"Search: {query}")
    inject = (
        f"Web search results for '{query}':\n{results}\n\n"
        "Answer using these results. Be concise."
    )
    state['messages'].append({'role': 'user', 'content': inject})

    def generate():
        for chunk in stream_ollama(state['messages']):
            try:
                obj = json.loads(chunk.strip())
                if obj.get('done') and obj.get('full'):
                    state['messages'].append({'role': 'assistant', 'content': obj['full']})
                    log(f"Cerberus (search): {obj['full'][:80]}")
            except Exception:
                pass
            yield chunk

    return Response(generate(), mimetype='text/plain',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


@app.route('/api/clear', methods=['POST'])
def api_clear():
    save_session()
    state['messages']    = [{'role': 'system', 'content': state['system_prompt']}]
    state['session_log'] = []
    log("Conversation cleared.")
    return jsonify({'ok': True})


@app.route('/api/memory', methods=['POST'])
def api_memory():
    note = (request.json or {}).get('note', '').strip()
    if not note:
        return jsonify({'error': 'no note'}), 400
    ok = update_memory(note)
    if ok:
        log(f"Memory updated: {note}")
    return jsonify({'ok': ok})


@app.route('/api/note', methods=['POST'])
def api_note():
    data  = request.json or {}
    note  = data.get('note', '').strip()
    agent = data.get('agent', '').lower().strip()
    if not note:
        return jsonify({'error': 'no note'}), 400
    try:
        os.makedirs(SHARED_DIR, exist_ok=True)
        notes_path = AGENT_NOTE_FILES.get(agent, os.path.join(SHARED_DIR, 'cerberus_notes.md'))
        ts = datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(notes_path, 'a', encoding='utf-8') as f:
            f.write(f"\n---\n{ts}\n{note}\n")
        log(f"Shared note ({agent or 'general'}): {note[:60]}")
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})


@app.route('/api/save', methods=['POST'])
def api_save():
    ok = save_session()
    return jsonify({'ok': ok})


@app.route('/api/model', methods=['POST'])
def api_model():
    model = (request.json or {}).get('model', '').strip()
    if model:
        state['model'] = model
        log(f"Model switched to: {model}")
    return jsonify({'ok': True, 'model': state['model']})


# -- init + launch ------------------------------------------------------------

def init():
    os.makedirs(UI_DIR,            exist_ok=True)
    os.makedirs(CERBERUS_SESSIONS, exist_ok=True)

    system_prompt, loaded = build_system_prompt()
    state['system_prompt'] = system_prompt
    state['loaded']        = loaded
    state['messages']      = [{'role': 'system', 'content': system_prompt}]

    log(f"Server started. Model: {state['model']}. Loaded: {', '.join(loaded)}")
    print(f"\nCerberus ready at http://localhost:{PORT}")
    print(f"Loaded: {', '.join(loaded)}")
    if not check_ollama():
        print("WARNING: Ollama is not running. Start it from the system tray.")


if __name__ == '__main__':
    init()
    app.run(host='127.0.0.1', port=PORT, debug=False, threaded=True)
