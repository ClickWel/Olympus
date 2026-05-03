# Hermes Agent Reference

## What It Is
Open-source AI agent framework by Nous Research. CLI-based, persistent memory, browser automation, file ops, terminal access, skills system, messaging gateway. Potential Cerberus replacement or teammate.

## Install Location
Config: `/home/click/.hermes/config.yaml`
API Keys: `/home/click/.hermes/.env`
Data: `/home/click/.hermes/cron/`, `sessions/`, `logs/`

## Current Config (2026-04-09)
- **Provider:** OpenRouter
- **Default model:** qwen/qwen3.6-plus:free
- **TTS:** ElevenLabs (keys in api-keys.md)
- **Search:** Tavily (key in api-keys.md)
- **Browser:** Local headless Chromium
- **Terminal backend:** Local
- **Max iterations:** 100
- **Tool progress:** all
- **Compression threshold:** 0.5
- **Session reset:** Inactivity + daily at 4am, 1440min timeout
- **Messaging gateway:** Discord (configured)

## Tools Enabled
- Web Search & Scraping
- Browser Automation
- Terminal & Processes
- File Operations
- Code Execution
- Vision / Image Analysis
- Image Generation (FAL.ai key in api-keys.md - needs setup)
- Text-to-Speech (ElevenLabs)
- Skills (list, view, manage)
- Task Planning
- Memory (persistent)
- Session Search
- Clarifying Questions
- Task Delegation
- Cron Jobs

## Tools NOT Enabled (yet)
- Mixture of Agents - worth enabling, lets Hermes delegate subtasks to other models
- RL Training
- Home Assistant

## Key Commands
```
hermes                  Start chatting
hermes setup            Re-run full setup wizard
hermes setup model      Change model/provider
hermes setup tools      Configure tool providers / add missing API keys
hermes setup gateway    Configure messaging (Discord etc.)
hermes config           View current settings
hermes config edit      Open config in editor
hermes doctor           Check for issues
hermes gateway          Start messaging gateway
```

## To-Do
- [ ] Enable Mixture of Agents via `hermes setup tools`
- [ ] Add FAL.ai key for image generation
- [ ] Add ElevenLabs key via `hermes setup tools`
- [ ] Test Discord gateway
- [ ] Evaluate vs Cerberus for task work

## API Keys (stored in D:\Olympus\reference\api-keys.md)
- OpenRouter
- Tavily
- ElevenLabs (x2)
- FAL.ai
- GitHub token
