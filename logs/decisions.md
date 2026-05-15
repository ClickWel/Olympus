# Decision Log

_Append-only. One entry per decision._

---

**2026-04-25** - CDP dual-browser pipeline moves to Ares Node.js (cdp_runner.js), not Atlas Python. Browser tool cannot address two browsers simultaneously. cdp_runner.js is the base for all future dual-browser IDOR work.

**2026-04-25** - IDOR findings go to /mnt/d/Ares/output/idor_findings/, not Hermes logs. Agent output stays in that agent's folder.

**2026-05-02** - Keep DISABLE_AUTOUPDATER enabled. Hy3/OpenRouter setup with custom plugins benefits from manual update control.

**2026-05-02** - Session End sequence updated: step 7 runs dx handoff skill to write HANDOFF.md. Session Start step 3 reads HANDOFF.md if present.

**2026-05-02** - attribution config uses object format {"commit":"","pr":""}, not boolean. Applies to both user and project settings.json.

---

## 2026-04-23

- Burp intercept stays OFF during Talos sessions to prevent request timeouts
- No VRAM Rainmeter widget - HWiNFO dependency is too much overhead; use `nvidia-smi dmon -s m -d 5` in terminal instead
- LM Studio is exclusive model runner going forward; Ollama/llama not in startup
- MSI Afterburner 4.6.6 installed and kept (GPU monitoring, potential OSD use)

## Format

```
[YYYY-MM-DD] - Decision: [what was decided] | Rationale: [why]
```

---

## Log

[2026-03-29] - Decision: Olympus set up as standalone CC project at D:\Olympus, running alongside D:\Clawdbot (not replacing it). | Rationale: Moltbot Argus still useful, no reason to delete anything. Additive only.
[2026-03-29] - Decision: Olympus tab color = green (#2ECC71). | Rationale: Jeff likes natural settings, Mount Olympus as a tree. Green fits the identity.
[2026-03-30] - Decision: No Moltbot gateway for inter-agent comms. | Rationale: D:\Shared + Jeff relay keeps Jeff in the loop. Direct socket removes oversight from the hierarchy.
[2026-03-30] - Decision: Voice skill parked indefinitely. | Rationale: Not needed. Trio-skill-opportunity.md is voice-only - revisit only if a specific use case comes up.
[2026-03-30] - Decision: 75k token threshold across all three agents. | Rationale: Cost-saving. Stop and offer session backup rather than dragging context forward.
[2026-03-30] - Decision: D:\Shared created as neutral trio drop zone. | Rationale: Clean handoff mechanism without needing live socket or Jeff to manually relay files.
[2026-03-30] - Decision: Olympus tab color updated to #2D6A2D (dark forest green). | Rationale: Jeff wanted "dark green like a 200 year old tree" - #2ECC71 was too bright/mint.
[2026-03-31] - Decision: Self-edit with mandatory report system adopted for Argus and Atlas. | Rationale: Memory captures facts but not behavior. Agents were drifting silently. Reports make changes visible and reviewable by Olympus.
[2026-03-31] - Decision: Silence = approval on self-edit reports. | Rationale: Reduces overhead. Olympus flags problems, not rubber-stamps good work.
[2026-03-31] - Decision: CLAUDE.md always wins over memory when they conflict. | Rationale: CLAUDE.md is behavior, memory is context. Clear hierarchy prevents confusion.
[2026-03-31] - Decision: Slack monitoring for cro-team-operations deferred. | Rationale: Jeff decided complexity not worth it for now. Lever integration remains an option if revisited.
[2026-04-07] - Decision: gemma4-26b-talos uses Ollama registry base not LM Studio GGUF. | Rationale: Ollama 0.20.3 does not support gemma4 architecture. Revisit when Ollama adds native support.
[2026-04-07] - Decision: Role switcher confirmation rule lives in CLAUDE.md only, not role files. | Rationale: Local models don't reliably read loaded files before responding. CLAUDE.md is the only guaranteed read.
[2026-04-07] - Decision: Script paths in role files use quoted forward slashes. | Rationale: Unquoted backslashes get concatenated to working directory by local models, producing broken paths.
[2026-04-07] - Decision: gemma4-26b ctx = 32k. | Rationale: Weights fit in 4070 Ti 12GB VRAM, KV cache overflow handled by 64GB system RAM. CPU offload not needed.
[2026-04-14] - Decision: Removed deepseek/deepseek-v3.2 from ai-gateway static catalog in Hermes models.py. | Rationale: Hermes was auto-routing the model to Vercel AI Gateway due to a wrong entry in _PROVIDER_MODELS. Model is on OpenRouter; static catalog was stale. Direct source edit, backed up as models.py.bak_20260414.
[2026-04-21] - Decision: Talos bug hunter context set to 87987 tokens (10.93GB VRAM) for both candidates. | Rationale: ~1GB headroom on 4070 Ti, matches OmniClaw stable range, avoids orphan process VRAM failures.
[2026-04-21] - Decision: OpenRouter 500 errors during compaction get 3 retries (5s apart) then fall back to main model. | Rationale: 500 is transient - blanking summary_model permanently would cause 2-3 min local compress every 5 min during heavy recon. Retry first, fall back only after repeated failure.
[2026-04-21] - Decision: Keeper dropped as bug bounty test target. | Rationale: Vault uses encrypted WebSocket, not REST. Automated sweep not viable. Next: Personio.
[2026-04-29] - Decision: WSL agents (Hermes/Ares/Talos on WSL) are legacy. New work is Windows-native only. Copy and rebuild rather than editing shared files. | Rationale: WSL crew still functional, don't break them, but don't maintain for them either.
[2026-04-29] - Decision: Skill name fields not renamed -- fuzzy search bridges the gap. | Rationale: Renaming risks breaking inter-skill references. Let the search layer handle short-name lookups.
[2026-04-29] - Decision: Default model for Hermes Desktop is openrouter/auto. MiniMax is backup only. | Rationale: Auto-router picks best available; hardcoding MiniMax was limiting quality unnecessarily.
[2026-05-02] - Decision: BB Loop cancelled, replaced by CC terminals (Hy3, Laguna) coached by Codex (OpenAI desktop agent). | Rationale: BB Loop was flaky and hit walls at account creation. CC terminals on free tiers with Codex coaching is simpler and more reliable.

[2026-05-07] - Decision: Optimal model assignments for Hack Team agents: Crypt=Laguna, Pwn=OSS20B, Recon=Gemini3, SICS=Laguna. | Rationale: Match model strengths to agent roles (reasoning, tool calling, speed, general).
[2026-05-07] - Decision: File structure - .bat files in agent directories (D:\Crypt, etc.), .lnk shortcuts in Hack Team folder only. | Rationale: Keeps launchers with their agents, desktop folder clean with just shortcuts.
[2026-05-07] - Decision: Use `start /min` approach for launching multiple agents from start-ctf-team.bat. | Rationale: Prevents extra cmd windows (8 total) by minimizing the wrappers, leaving only 4 agent terminals.
[2026-05-07] - Decision: Keep Hy3 and Owl as legacy model options alongside newer models. | Rationale: They were working well previously, user wants them available as alternatives.

[2026-05-13] - Decision: CPR (compress/preserve/resume) wired into session end protocol for all agents. | Rationale: Replaces manual session file writes with structured, searchable AI memory logs. Reduces token cost between sessions.
[2026-05-13] - Decision: Obsidian vault at D:\Obsidian is cross-agent knowledge base. Each agent maintains D:\Obsidian\agents\[name].md as a standing note, overwritten each session end. | Rationale: Enables cross-agent intel sharing without Jeff having to relay information manually.
[2026-05-13] - Decision: dx:handoff stays in session end protocol alongside CPR. | Rationale: Handoff is the human relay note for Jeff. CPR is the AI memory record. Different jobs, both needed.
[2026-05-13] - Decision: BB laguna variant added for all 4 hack team agents (poolside/laguna-m.1:free on OpenRouter). GLM-5.1 dropped - NVIDIA NIM not CC-compatible. | Rationale: OpenRouter free models work in CC, direct provider APIs do not.

[2026-05-14] - Decision: Qwen Code gets all provider keys self-contained in ~/.qwen/settings.json env block. | Rationale: Was leaking OPENROUTER_API_KEY from system environment (loaded by clawdbot-dev). Self-contained is cleaner and portable.
