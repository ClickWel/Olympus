# Trio Launch Architecture
Last updated: 2026-04-17

## Overview

One binary, three profiles. All three agents (Hermes, Ares, Talos) run the same
hermes-agent binary installed in a shared Python 3.11 venv. Profile isolation
handles the rest.

## Binary Chain

```
/home/click/.local/bin/hermes         <- symlink to venv binary (Hermes default)
/home/click/.local/bin/ares           <- 2-line wrapper: exec hermes -p ares
/home/click/.local/bin/talos          <- does not exist; talos.sh calls hermes --profile talos directly
```

Real binary: `/home/click/.hermes/hermes-agent/venv/bin/hermes` (Python 3.11)
Installed via: `/home/click/.hermes/hermes-agent/venv/bin/python3 -m pip install -e /home/click/.hermes/hermes-agent`

## Profile Layout

```
/home/click/.hermes/                  <- Hermes (default profile)
    SOUL.md
    config.yaml
    .env
    skills/                           <- shared skill folder (all agents read here)

/home/click/.hermes/profiles/ares/   <- Ares profile
    SOUL.md
    config.yaml
    .env
    skills -> /home/click/.hermes/skills   (symlink)

/home/click/.hermes/profiles/talos/  <- Talos profile
    SOUL.md
    config.yaml
    .env
    skills -> /home/click/.hermes/skills   (symlink)
```

Hermes uses the root as its home. Ares and Talos use named profile dirs.
There is no profiles/hermes/ - Hermes IS the root.

## Launch Scripts

All three wrappers delegate to the shared core:

```
/home/click/launch-agent.sh           <- shared core (edit this for system-wide changes)
/home/click/launch-hermes-audio.sh   <- redirects stderr to log, then calls launch-agent.sh hermes
/home/click/launch-ares-audio.sh     <- calls launch-agent.sh ares
/home/click/launch-talos.sh          <- calls launch-agent.sh talos --profile talos
```

What launch-agent.sh does (in order):
1. Sources .profile and .bashrc
2. Detects Windows host IP via default route
3. Sets PULSE_SERVER=tcp:<host>:4713
4. Sets BROWSER_CDP_URL if Chrome CDP is reachable on :9222
5. Writes PID to D:\Shared\reports\<agent>_pid.txt
6. Traps EXIT/INT/TERM/HUP to clean up PID file
7. Verifies binary exists (hard fail)
8. Verifies SOUL.md exists for profile agents (hard fail)
9. Waits up to 10s for PulseAudio on :4713
10. Exec the agent binary

## Windows Launch Chain (Ares example)

```
Desktop shortcut -> D:\Ares\start-ares.bat
  -> wscript D:\Ares\launch_ares_invisible.vbs
    -> D:\PulseAudio\start-pulse.bat (sync, hidden)
    -> Windows Terminal: wsl -e bash /home/click/launch-ares-audio.sh
```

Hermes and Talos have equivalent chains at D:\Hermes\ and D:\Talos\.

## D: Drive Role

D: drive is working storage - scripts, targets, session logs, knowledge bases.
NOT config, NOT SOUL files, NOT skills. Those live in WSL.

```
D:\Ares\          <- Ares working area (sessions, scripts, targets, knowledge)
D:\Talos\         <- Talos working area (sessions, memory, models, scripts)
D:\Hermes\        <- Hermes working area (scripts, targets, projects)
D:\Shared\        <- Inter-agent shared space (reports, handoffs, copy_output.txt)
```

## Models

- Hermes: minimax/minimax-m2.7 via OpenRouter
- Ares: minimax/minimax-m2.7 via OpenRouter
- Talos: local LM Studio at http://10.0.0.25:1234/v1
  - Default in config: google/gemma-4-e4b
  - Alias "qwen": qwen/qwen3.5-9b (load manually in LM Studio when needed)

## Secrets

All secrets in .env files, never in config.yaml.
NOTION_TOKEN referenced in config.yaml as ${NOTION_TOKEN}, value in .env.

## If Something Breaks

| Symptom | Check |
|---|---|
| Import error on launch | Reinstall: `venv/bin/python3 -m pip install -e /home/click/.hermes/hermes-agent` |
| 400 error (Talos) | ANTHROPIC_BASE_URL missing - check launch script env |
| 500 error (Talos) | Check LM Studio - model not loaded or OOM |
| Audio not working | Is PulseAudio running? Check D:\PulseAudio\start-pulse.bat |
| Agent not found | Check /home/click/.local/bin/<agent> exists and is executable |
| SOUL error on launch | SOUL.md missing from profile dir - restore from D:\tmp\backups_longterm\ |
