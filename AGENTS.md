# AGENTS.md - Olympus

Olympus is the infrastructure manager for the Clawdbot trio (Olympus, Argus, Atlas).
Jeff is the owner. Final say on everything.

## Directory permissions

Read freely: `D:\Olympus`, `D:\Atlas`, `D:\Cerberus`, `D:\Clawdbot`, `D:\Shared`, `D:\Talos`.
Write freely: `D:\Talos`, `D:\Shared`.
Create/modify scripts: ask first.
Shell write commands: require approval.

## Core Rules (Windows)

- Open files with `encoding='utf-8'`
- No `python -c` one-liners; write a .py file and run it
- No emoji in terminal print statements
- Use `curl.exe` not `curl` on Windows
- Script paths: `python "D:/path/script.py"`
- Find local files with Glob/Grep; never ask Jeff for a path you can search for

## Shell guard

Git Bash exports `SHELL=/bin/bash.exe` to child processes, breaking Claude Code shell detection on Windows.
All `.bat` launchers must call `D:\Olympus\scripts\claude-code-windows-shell.bat` first to force PowerShell.

## Vision tool

When screenshots are attached:
```
powershell -ExecutionPolicy Bypass -File "D:/Olympus/vision/analyze-image.ps1" "<image-path>"
```

## Compaction control (Hy3 via OpenRouter)

Set environment variables to control trigger:
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` - compaction trigger percentage
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS` - max context window size

## Session protocol

Full session start/end procedures are in `CLAUDE.md`.
Key files to read at session start:
- `memory/MEMORY.md`
- `plans/active_plan.md`
- Most recent file in `sessions/`
- `D:/Shared/reports/` for agent self-edit reports

Session end: write summary to `sessions/YYYY-MM-DD.md`, update `memory/MEMORY.md` and `plans/active_plan.md`, log to `logs/decisions.md`, copy session file to `backups/`.

## Secrets never committed

`.gitignore` protects: `MASTER_API_KEYS.env`, `scripts/**/nr_introspect*.ps1`, `memory/talos_500_fix.md`.
