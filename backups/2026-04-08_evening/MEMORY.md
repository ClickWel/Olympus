# Olympus Local Memory
_Written and maintained by Olympus across sessions._

## Jeff Profile
- Jeff (Click/ClickWell) - CRO Operator at Convert Like Crazy
- Voice dictation user - messages may be unpunctuated
- Ask, never assume on anything consequential
- Session end triggers: "see ya" / "later dude" / "we're done"

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

## Open Items
- Trio skill opportunity: moltbot agent interface. See `D:\Clawdbot\Argus_Share\trio-skill-opportunity.md`

## Team Model Assignments (Finalized)
- **Olympus (Infrastructure/Brain)**: Nemotron 3 Super Free (primary for deep work) OR Gemini Flash Latest (for vision-dependent tasks)
- **Atlas (Execution/Revenue)**: Gemini Flash Latest (stable, fast, tool-capable with vision)
- **Argus (Reporting/Ops)**: Gemini Flash Latest (speed + vision for board/screen reading)
- **Local Power (VRAM)**: Qwen2.5-Coder:14b (elite coding), Ministral-3:8b (stable generalist)
- **Cloud Fallback**: Gemini Flash Latest (proven connection stability + vision)
- **Local Fallback**: gemma4-26b (precision logic, no vision)
- **Vision Tool**: D:\Olympus\vision\analyze-image.ps1 (qwen2.5vl:3b primary, Gemini fallback)
