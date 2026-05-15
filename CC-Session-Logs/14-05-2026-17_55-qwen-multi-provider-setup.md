# Session Log: 14-05-2026 17:55 - qwen-multi-provider-setup

## Quick Reference (for AI scanning)
**Confidence keywords:** qwen, qwen-code, settings.json, modelProviders, env, OPENROUTER_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, NVIDIA_API_KEY, OPENAI_API_KEY, DEEPSEEK_API_KEY, GITHUB_TOKEN, CLOD_API_KEY, multi-provider, model-picker, duplicate-id-bug
**Projects:** D:\Qwen, ~/.qwen/settings.json, MASTER_API_KEYS.env
**Outcome:** Qwen Code configured with 9 providers and 30+ models, all keys self-contained; duplicate model ID bug identified as cause of models disappearing from picker.

---

## Decisions Made
- Qwen Code gets all provider keys in its own `env` block in `~/.qwen/settings.json` - no longer leaks from system environment or clawdbot-dev
- All providers added: OpenRouter, Anthropic, OpenAI, DeepSeek, Groq, Google, NVIDIA, GitHub Models, Clod
- Duplicate model IDs exist (gpt-4o appears for both OpenAI direct and GitHub Models; claude-sonnet-4-6 appears for both Anthropic and Clod) - fix deferred to next session

## Key Learnings
- Qwen Code was picking up `OPENROUTER_API_KEY` from the system environment (loaded by clawdbot-dev bat launchers), not from its own config - all models using that key worked but the dependency was invisible
- Qwen Code removes models from the picker after they error or fail - models disappearing after first use is likely caused by duplicate `"id"` fields across providers, not the providers themselves being broken
- Qwen's `modelProviders.openai` array accepts any OpenAI-compatible endpoint via `baseUrl` + `envKey` - works for Groq, NVIDIA, Google Gemini compat, GitHub Models, DeepSeek, Clod all the same way
- Anthropic direct API (`api.anthropic.com/v1`) may not work cleanly in Qwen since it uses `/v1/messages` not `/v1/chat/completions` - OpenRouter's Anthropic models are the safer fallback

## Files Modified
- `C:\Users\click\.qwen\settings.json`: Full rewrite - added 9 provider keys to `env` block, expanded modelProviders from 13 to 30+ entries across OpenRouter, Anthropic, OpenAI, DeepSeek, Groq, Google, NVIDIA, GitHub Models, Clod

## Setup & Config
- **Qwen config location:** `C:\Users\click\.qwen\settings.json`
- **Qwen launcher:** `C:\Users\click\Desktop\Qwen.lnk` -> `D:\Qwen\start-qwen.bat` -> runs `qwen` from `D:\Qwen`
- **Key sources:** `D:\Shared\MASTER_API_KEYS.env` and `D:\Olympus\MASTER_API_KEYS.env`
- **Provider endpoints added:**
  - OpenRouter: `https://openrouter.ai/api/v1`
  - Anthropic: `https://api.anthropic.com/v1`
  - OpenAI: `https://api.openai.com/v1`
  - DeepSeek: `https://api.deepseek.com/v1`
  - Groq: `https://api.groq.com/openai/v1`
  - Google: `https://generativelanguage.googleapis.com/v1beta/openai`
  - NVIDIA: `https://integrate.api.nvidia.com/v1`
  - GitHub Models: `https://models.github.ai/inference`
  - Clod: `https://api.clod.io/v1`
- **Known issue:** Duplicate model IDs (`gpt-4o`, `claude-sonnet-4-6`) cause models to vanish from picker after first use. Fix: rename to `gpt-4o-github`, `claude-sonnet-4-6-clod` etc.

---

## Quick Resume Context
Qwen Code is now configured with 9 providers and all keys are self-contained in `~/.qwen/settings.json`. The main remaining issue is duplicate model IDs - two entries both use `"id": "gpt-4o"` (OpenAI and GitHub Models) and two use `"id": "claude-sonnet-4-6"` (Anthropic and Clod), which causes Qwen to drop one from the picker after the first is tested. Fix is straightforward: give each entry a unique ID string regardless of what the provider calls it.

---

## Raw Session Log

**Jeff:** right now qwen only launched with one api loaded, how do i add multiple so i can switch between anthropic and openrouter and github, for example, whenever i want? - D:\Qwen

**Olympus:** [Read D:\Qwen, found start-qwen.bat and CLAUDE.md. Read ~/.qwen/settings.json - found only one key in env block (QWEN_CUSTOM_API_KEY_...), all other OR models using OPENROUTER_API_KEY which wasn't defined there. Explained the structure and asked for keys before writing.]

**Jeff:** But why the heck is it using the clawdbot? env?

**Olympus:** Explained that models with `"envKey": "OPENROUTER_API_KEY"` were falling back to system environment, which had the key loaded by clawdbot-dev bat launchers. Fix: add OPENROUTER_API_KEY directly to Qwen's own env block.

**Jeff:** Yeah. I like this DUI, and I wanna keep on using this. So let's set Gwen up with whatever he needs. Pardon the mistakes. This is speech to text. So let's set him up with whatever he needs, including settings, environment, whatever.

**Olympus:** [Read MASTER_API_KEYS.env from both D:\Shared and D:\Olympus. Found all keys. Added Anthropic, GitHub Models, OpenAI entries to settings.json plus their keys in env block.]

**Jeff:** but those three were just examples, i wanted the other options for free models too like nvidia, google, groq... ect

**Olympus:** [Re-read both MASTER_API_KEYS.env files. Found Google, Groq, NVIDIA, DeepSeek, Clod keys. Rewrote settings.json entirely with all 9 providers, 30+ models.]

**Jeff:** C:\Users\click\Desktop\Qwen.lnk is that the same qwen that i open from the desktop lnk? because that loads this like normal, is that expected? [screenshot of Qwen Code v0.15.11 showing inclusionai/ring-2.6-1t:free as active model]

**Olympus:** Yes, same Qwen. Showing ring-2.6-1t:free is correct - that's the default. Type /model to switch.

**Jeff:** Any idea why after I try a certain model and test it, and then go to a different model to test, that that first model I tested is no longer available to me?

**Olympus:** Identified two causes: (1) Qwen drops models from picker after errors, (2) duplicate IDs - gpt-4o and claude-sonnet-4-6 both appear twice with different providers, Qwen deduplicates on ID. Fix: rename duplicate entries to unique IDs like gpt-4o-github, claude-sonnet-4-6-clod.

**Jeff:** end session
