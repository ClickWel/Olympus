# Handoff — 2026-05-17
**Olympus → Jeff**

## What Was Done

Diagnosed and fully fixed the curl blocking issue affecting all Crush agents. Root cause was missing `.crush/crush.json` in each agent's working directory - Crush uses an allowlist, so without the file agents had no tool permissions. Deployed crush.json to all 12 agent directories (hack team x8, Olympus, Atlas, Talos, Crush base). Also expanded the tool set across all agents to include glob, think, and mcp (Docker MCP was already connected but unused).

Hit a BOM encoding bug - PowerShell's `Set-Content -Encoding UTF8` adds a UTF-8 BOM that Crush's JSON parser rejects. Fixed by switching to `[System.IO.File]::WriteAllText` with explicit no-BOM encoder.

Also briefly pursued a crushfetch.exe workaround (curl renamed), but isolated and confirmed the crush.json fix was the real solution. Rolled crushfetch back completely - no junk left behind.

## Current State

All Crush agents fully operational with complete tool set:
- `bash`, `view:read`, `edit:write`, `ls`, `grep`, `fetch`, `glob`, `think`, `mcp`
- curl.exe works natively via bash in all agents
- Docker MCP (8 tools) available to all agents
- No crushfetch workaround - clean

Agents confirmed working: Crypt, Crypt_BB, Pwn, Pwn_BB, Recon, Recon_BB, SICS, Sics_BB, Crush, Olympus, Atlas, Talos

## What Worked
- Deploying `.crush/crush.json` per agent directory (not symlinked - separate files for flexibility)
- `[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))` for BOM-free JSON writes from PowerShell
- Isolating which fix was doing the work before cleaning up (Jeff insisted, correct call)

## What Didn't Work
- `Set-Content -Encoding UTF8` in PowerShell - adds BOM, breaks Crush JSON parser
- CRUSH.md system prompt instructions alone - model acknowledged the rule but Crush's executor still blocked at the tool level
- crushfetch.exe rename workaround - unnecessary once root cause found

## Next Steps
1. If any new agent directory gets a Crush launcher, deploy crush.json immediately using the no-BOM method
2. Crush bat restructure (carry-over from 2026-05-15 handoff) - still pending
3. Optionally install LSP servers (pyright, gopls) for better code analysis in Crush
