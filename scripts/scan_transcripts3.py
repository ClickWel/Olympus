import json
import re
from collections import Counter
import sys

bash_commands = Counter()
mcp_tools = Counter()

# Auto-allowed commands (no need to add to allowlist)
AUTO_ALLOWED = {
    'cat', 'head', 'tail', 'wc', 'ls', 'find', 'pwd', 'whoami', 'echo', 'printf',
    'git status', 'git log', 'git diff', 'git show', 'git branch', 'git blame',
    'git remote', 'git rev-parse', 'git describe', 'git stash list', 'git reflog',
    'git shortlog', 'git worktree list',
    'gh pr view', 'gh pr list', 'gh pr diff', 'gh pr checks', 'gh pr status',
    'gh issue view', 'gh issue list', 'gh issue status',
    'gh run view', 'gh run list', 'gh workflow list', 'gh workflow view',
    'gh repo view', 'gh release view', 'gh release list', 'gh auth status',
    'grep', 'rg', 'jq', 'ps', 'df', 'du', 'date', 'hostname', 'uname',
    'id', 'free', 'nproc', 'basename', 'dirname', 'realpath', 'which', 'type',
    'stat', 'strings', 'od', 'nl', 'readlink', 'diff', 'seq',
    'xargs', 'file', 'sort', 'sed', 'tree', 'base64', 'history', 'arch',
    'cal', 'uptime', 'cd', 'groups', 'locale',
}

# Commands that are NEVER read-only (dangerous)
DANGEROUS = {
    'rm', 'del', 'mv', 'cp', 'mkdir', 'touch', 'git push', 'git merge',
    'git commit', 'git add', 'git checkout', 'git reset', 'git rebase',
    'npm publish', 'npm install', 'npm ci', 'pnpm install', 'yarn install',
    'pip install', 'pip3 install',
    'npx', 'bunx', 'uvx', 'uv',
    'python', 'python3', 'node', 'bun', 'deno', 'ruby', 'perl', 'php', 'lua',
    'bash', 'sh', 'zsh', 'fish', 'powershell', 'powershell.exe', 'cmd', 'cmd.exe',
    'npm run', 'yarn run', 'pnpm run', 'bun run', 'make', 'just',
    'cargo run', 'go run',
    'gh pr create', 'gh pr merge', 'gh issue create', 'gh release create',
    'gh api',
    'docker run', 'docker exec', 'kubectl exec', 'sudo',
    'ssh', 'scp', 'rsync',
    'curl.exe', 'curl', 'wget', 'invoke-webrequest', 'iwr',
    'for', 'foreach', 'while', 'do', 'if', 'else', 'switch',
    'start', 'invoke-expression', 'iex',
}

def get_base(cmd_str):
    """Extract the base command from a full command string."""
    if not cmd_str:
        return None
    # Remove env var assignments
    cleaned = re.sub(r'^\s*\w+=\S+\s+', '', cmd_str)
    # Remove sudo, timeout, time prefixes
    cleaned = re.sub(r'^\s*(sudo|timeout\s+\S+|time)\s+', '', cleaned)
    # Take first command in chain (&&, ||, ;)
    cleaned = re.split(r'\s*(&&|\|\||;)\s*', cleaned)[0]
    # Take first command in pipe
    cleaned = cleaned.split('|')[0].strip()
    # Remove command substitution
    cleaned = re.sub(r'`[^`]*`', '', cleaned)
    cleaned = re.sub(r'\$\([^)]*\)', '', cleaned)
    # Remove quotes
    cleaned = cleaned.strip('"\'')
    parts = cleaned.split()
    if not parts:
        return None
    cmd = parts[0]
    # For git/gh/docker, include subcommand
    if cmd in ('git', 'gh', 'docker') and len(parts) >= 2:
        return f"{cmd} {parts[1]}"
    return cmd

def is_read_only(cmd_str):
    """Check if a bash command is read-only."""
    base = get_base(cmd_str)
    if not base:
        return False
    # Check dangerous commands - exact match or starts with "cmd "
    for d in DANGEROUS:
        if base == d or base.startswith(d + ' '):
            return False
    return True

# Read file paths from command-line arguments
filepaths = sys.argv[1:]
if not filepaths:
    filepaths = [line.strip() for line in sys.stdin if line.strip()]

total_lines = 0
assistant_msgs = 0
tool_uses = 0

for filepath in filepaths:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                total_lines += 1
                try:
                    obj = json.loads(line)
                    if obj.get('type') != 'assistant':
                        continue
                    assistant_msgs += 1
                    message = obj.get('message', {})
                    content = message.get('content', [])
                    if not isinstance(content, list):
                        continue
                    for item in content:
                        if not isinstance(item, dict):
                            continue
                        if item.get('type') != 'tool_use':
                            continue
                        tool_uses += 1
                        tool_name = item.get('name', '')
                        if tool_name == 'Bash':
                            inp = item.get('input', {})
                            if isinstance(inp, dict):
                                cmd = inp.get('command', '')
                                if cmd and is_read_only(cmd):
                                    base = get_base(cmd)
                                    if base and base not in AUTO_ALLOWED:
                                        bash_commands[base] += 1
                        elif tool_name.startswith('mcp__'):
                            tool_lower = tool_name.lower()
                            if any(w in tool_lower for w in ['read', 'get', 'list', 'search', 'view', 'find', 'fetch', 'query']):
                                mcp_tools[tool_name] += 1
                except (json.JSONDecodeError, Exception):
                    continue
    except (IOError, Exception):
        continue

print(f"DEBUG: Processed {total_lines} lines, found {assistant_msgs} assistant msgs, {tool_uses} tool uses")
print(f"DEBUG: Unique bash commands found: {len(bash_commands)}")

print("\n=== BASH COMMANDS (read-only, not auto-allowed) ===")
for cmd, cnt in bash_commands.most_common(50):
    print(f"{cnt}\t{cmd}")

print("\n=== MCP TOOLS (read-only) ===")
for tool, cnt in mcp_tools.most_common(50):
    print(f"{cnt}\t{tool}")
