# Olympus Local Memory
_Written and maintained by Olympus across sessions._

## Jeff Profile
- Jeff (Click/ClickWell) - CRO Operator at Convert Like Crazy
- Voice dictation user - messages may be unpunctuated
- Ask, never assume on anything consequential
- Session end triggers: "wrap up" / "end session" / "save and close" / "see ya" / "later dude" / "we're done" / "restarting"

## The Hierarchy
- Jeff = owner (final say on everything)
- Olympus = boss (manages Argus and Atlas on Jeff's behalf)
- Argus + Atlas = employees (escalate through Jeff to Olympus when they need something)

| Name    | Role                          | Location      | Color  | Reports to         |
|---------|-------------------------------|---------------|--------|--------------------|
| Argus   | Watches the board, voice PTT  | D:\Argus      | Cyan   | Olympus (via Jeff) |
| Atlas   | Hunts revenue, executes       | D:\Atlas      | Gold   | Olympus (via Jeff) |
| Olympus | Boss - infrastructure manager | D:\Olympus    | Green  | Jeff directly      |

## System Layout
- Codebase: `D:\Clawdbot`
- Runtime: `C:\Users\click\.clawdbot-dev`
- Shared drop folder: `D:\Clawdbot\Argus_Share`
- Skills: `D:\Clawdbot\skills\`

## Key Preferences
- Flag large tasks before starting (~5-8k tokens. Worth it?)
- No em dashes in responses
- Max 2 retries on any error - stop and report after that
- Always open files with encoding='utf-8'
- No emoji in terminal print statements

## Talos/Hermes Config Notes
- 500 on compaction = check `providers:` block in talos config. Key detail: `summary_provider: openrouter` but `providers: {}` = unauthenticated, always 500. Fix: add openrouter key under providers. See `memory/talos_500_fix.md`.
- Backup before any config edit: `cp config.yaml config.yaml.bak-YYYYMMDD-HHMMSS`

## Session Protocol
- Session End step 7: runs dx handoff skill to write/update `HANDOFF.md` (goal, progress, what worked, what didn't, next steps)
- Session Start step 3: reads `HANDOFF.md` if it exists in project root
- handoff skill lives at: `C:/Users/click/.claude/plugins/cache/ykdojo/dx/0.14.12/skills/handoff/`

## Open Items
- Trio skill opportunity: moltbot agent interface. See `D:\Clawdbot\Argus_Share\trio-skill-opportunity.md`
- BB Worker Pipeline: CC terminals (Hy3, Laguna) coached by Codex. Replaces cancelled BB Loop.

## Completed (2026-05-02)
- Shell guard fix: Added `call D:\Olympus\scripts\claude-code-windows-shell.bat` to 24 Windows Claude Code launcher bats to force PowerShell instead of bash. Verified by Sonnet. Report: `D:\Shared\core\protocols\shell-fix-plan.md`
- BB Loop cancelled: Replaced with CC terminals (Hy3, Laguna) on free tiers, coached by Codex (OpenAI desktop agent). Flaky loop with account creation walls is dead.

## Completed (2026-05-07)
- Hack Team launcher setup: Created 5 launchers per agent (Crypt, Pwn, Recon, SICS) with models: Hy3, Laguna, Owl, OSS20B, Gemini3
- File structure: `.bat` files in agent directories (`D:\Crypt`, etc.), `.lnk` shortcuts in `C:\Users\click\Desktop\Hack Team\`
- Optimal model assignments: Crypt=Laguna, Pwn=OSS20B, Recon=Gemini3, SICS=Laguna
- `start-ctf-team.bat` launches all agents with optimal models using `start /min` approach
- Lesson: Keep solutions simple - `/min` flag prevents extra cmd windows vs complex wt.exe multi-tab commands

## Completed (2026-05-09)
- Hy3 removed from OpenRouter. Replaced with Ring 2.6 (inclusionai/ring-2.6-1t:free) as main model for CTF and BB teams
- Created start-ring-2.6.bat (CTF) and start-ring-2.6-bb.bat (BB) in all 4 agent dirs (Crypt, Pwn, Recon, SICS)
- Updated start-ctf-team.bat, start-selector.bat, create-ctf-shortcuts.ps1
- Desktop shortcuts created for all ring-2.6 and ring-2.6-bb launchers

## Team Model Assignments (Finalized)
- **Olympus (Infrastructure/Brain)**: Nemotron 3 Super Free (primary for deep work) OR Gemini Flash Latest (for vision-dependent tasks)
- **Atlas (Execution/Revenue)**: Gemini Flash Latest (stable, fast, tool-capable with vision)
- **Argus (Reporting/Ops)**: Gemini Flash Latest (speed + vision for board/screen reading)
- **Local Power (VRAM)**: Qwen2.5-Coder:14b (elite coding), Ministral-3:8b (stable generalist)
- **Cloud Fallback**: Gemini Flash Latest (proven connection stability + vision)
- **Local Fallback**: gemma4-31b (precision logic, high reliability, vision capable)
- **Vision Tool**: D:\Olympus\vision\analyze-image.ps1 (qwen2.5vl:3b primary, Gemini fallback)

## CTF Labyrinth Challenge (2026-05-06)
- Target: 154.57.164.80:30562 (alternate, original down)
- Status: Incomplete - remote binary differs from local (100 vs 40 doors)
- Local MD5: 23fe15de98472acc0fbd3a586805791c
- Finding: "69" triggers vulnerable path but overflow fails to execute escape_plan
- Next: Obtain remote binary, verify ASLR/PIE, try ROP to system()

## Session History: Trio Awakening (2026-04-09)
- **HQ Migration**: Moved from terminal to hybrid OpenCode Desktop App + standalone CLI (v1.4.0).
- **Workspace Isolation**: Established `D:\Argus`, `D:\Atlas`, and `D:\Olympus` with dedicated `AGENTS.md` souls.
- **Infrastructure**: Added CLI binary to `D:\Talos\bin` and created desktop launchers.
- **Coordination**: Implemented `D:\Shared\handoff.md` (transactional) and `D:\Shared\mission_control.md` (strategic hub).
- **Model Benchmarking**: Verified Big Pickle for deep work, Gemini Flash Lite for speed, and Gemma 4 31B as the "Reliable Deputy."
- **Vision Integration**: Set up `/vision` command for all agents to use cloud-based visual analysis.
- **Microsoft To-Do removed**: Argus attempted to use Microsoft To-Do integration, found expired tokens, looped and burned tokens. Jeff confirmed Microsoft To-Do is no longer in use. Removed all references from `D:\Argus\AGENTS.md`. The skill still exists at `D:\Clawdbot\skills\microsoft-todo\` but is dead code.

