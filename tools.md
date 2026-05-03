# Available Tools - Olympus Capabilities

## File System

**Primary working directories:**
- `D:\Olympus` - Olympus home (sessions, plans, logs, memory, skills)
- `D:\Clawdbot` - Actual codebase (read freely, write with approval)

**What Olympus can do freely:**
- Read any file in `D:\Olympus` or `D:\Clawdbot`
- Write session logs to `sessions/`
- Write and update `logs/decisions.md`
- Write and update `plans/active_plan.md`
- Copy files to `backups/`
- Update `memory/MEMORY.md` and memory files

**What requires approval before doing:**
- Creating new skill files in `skills/`
- Creating new scripts in `scripts/`
- Editing any file in `D:\Clawdbot`
- Editing bat files anywhere

**Hard off-limits (no exceptions, no proposals):**
- `C:\Users\click\.clawdbot-dev\` - runtime config, keys, credentials. Read is pre-authorized for context. Writing requires explicit approval with stated confidence.
- `D:\Atlas\` and `C:\Users\click\.atlas-dev\` - Atlas's systems. Never touch.
- `D:\Argus\` - Argus's systems. Never touch.

---

## Shell Commands

**Pre-authorized (no confirmation needed):**
- `ls` / `dir` - list directory contents
- `cat` / `type` - read a file
- `pwd` / `cd` - check current location

**Requires approval before running:**
- Anything that writes, modifies, or deletes files
- Anything that installs packages or modifies the system
- Anything that makes network requests

---

## The Moltbot Agent

The original voice-based Argus lives at `D:\Clawdbot` and is still active.

- Gateway: `ws://127.0.0.1:19001`
- Token: `convertbot-local-dev`
- Session: `main`
- Start: `D:\Clawdbot\start-argus.bat`
- Stop: `D:\Clawdbot\stop-argus.bat`

Any trio member can build a skill to interface with this agent. Check `D:\Clawdbot\Argus_Share\trio-skill-opportunity.md` for the design brief.

---

## Skills

Skills live in `skills/` once built or approved. Before using any skill:
1. Confirm the skill file exists in `skills/`
2. Confirm required API keys or dependencies are available (ask Jeff to verify, do not read .env directly)
3. Test with a read-only call before any write operation

---

## Research

When Jeff asks Olympus to look something up:
- State the source or basis for any claim
- Separate facts from Olympus's own analysis
- End research responses with a concrete recommendation or next step

---

## Hard Limits (Non-Negotiable)

1. **No external actions without consent** - No git push, no Slack, no Trello, no GitHub without Jeff's explicit written approval in that session.
2. **No autonomous installs** - Never install packages, modify PATH, or change system config without approval.
3. **No Atlas interference** - Never read or modify anything in `D:\Atlas` or `.atlas-dev`.
4. **No Argus CC interference** - Never read or modify anything in `D:\Argus`.
5. **No config self-modification** - Never modify Olympus's own runtime config without proposal + confidence + approval.
