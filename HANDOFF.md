# Handoff - 2026-05-15

## Goal

Install and wire up Vix (AI coding specialist, #1 on Terminal-Bench 2.0) as a new team member with a desktop shortcut launcher.

---

## Current Session - Vix Onboarding (IN PROGRESS)

### What Was Done
- Researched Vix: getvix.dev, github.com/kirby88/vix-releases - purpose-built coding agent, token-efficient, single-thread caching, virtual file system
- Installed Vix v0.2.2 in WSL Ubuntu: `vix` and `vixd` at `/usr/local/bin/`
- Confirmed Vix has interactive TUI mode (`vix` with no args = full chat interface)
- Created `D:\Vix\` as Vix's home folder
- Customized `~/.vix/agents/general.md` in WSL with Olympus personality, team roster, key paths - copy at `D:\Vix\vix-general.md`
- Created `D:\Vix\start-vix.bat` and `C:\Users\click\Desktop\Vix.lnk`

### What Worked
- `vixd &` then `vix` in WSL terminal launches the TUI correctly - confirmed working
- API key: `ANTHROPIC_API_KEY=***REMOVED***`
- Custom agent prompt installed successfully
- Windows Terminal path: `C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_1.24.10921.0_x64__8wekyb3d8bbwe\wt.exe`

### What Didn't Work
- `wt` not in PATH - must use full path to wt.exe
- `wt ... bash -c "cmd1; cmd2; cmd3"` - wt splits on semicolons and opens each as a separate tab. The final `exec vix` tab errored with "system cannot find the file specified"
- Shortcut pointing to bat directly - flashed and closed. Fixed by pointing shortcut to `cmd.exe /c bat`

### Current State of start-vix.bat
```
@echo off
"C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_1.24.10921.0_x64__8wekyb3d8bbwe\wt.exe" --title "Vix" --tabColor "#7B2FBE" wsl -d Ubuntu -e bash -c "export ANTHROPIC_API_KEY=...; pgrep vixd >/dev/null 2>&1 || vixd >/tmp/vixd.log 2>&1 & sleep 1 && cd /mnt/d/Vix && vix"
```
This still may split on semicolons. Not tested yet - session ended before retry.

---

## Next Steps

1. **Fix the bat launcher** - The semicolon-splitting problem. Solution: write a small bash script to `/mnt/d/Vix/launch.sh`, make it executable, and call that from wt instead of an inline bash -c string. Like this:

   `launch.sh`:
   ```bash
   #!/bin/bash
   export ANTHROPIC_API_KEY=***REMOVED***
   pgrep vixd >/dev/null 2>&1 || vixd >/tmp/vixd.log 2>&1 &
   sleep 1
   cd /mnt/d/Vix
   exec vix
   ```

   `start-vix.bat`:
   ```
   @echo off
   "C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_1.24.10921.0_x64__8wekyb3d8bbwe\wt.exe" --title "Vix" --tabColor "#7B2FBE" wsl -d Ubuntu -- bash /mnt/d/Vix/launch.sh
   ```

2. **Test the shortcut** - Click `Vix.lnk` on desktop, confirm purple WT tab opens with Vix TUI
3. **Add Vix to memory** - Save to `C:\Users\click\.claude\projects\D--Olympus\memory\` as a new agent entry

---

## Prior Session (2026-05-14) - Qwen Multi-Provider Setup

### Known Bug Still Open
- Duplicate model IDs in `C:\Users\click\.qwen\settings.json` - rename `gpt-4o` (GitHub) to `gpt-4o-github` and `claude-sonnet-4-6` (Clod) to `claude-sonnet-4-6-clod`

### Other Open Items
- Rotate NVIDIA API key (was exposed in prior conversation) - build.nvidia.com
- HermesDesktop: STT/voice (F9), three-way collab test, sidebar label hardcode
- BB targets: Atlas has Swapcard SSRF in progress on YWH

---

## Key Paths

- Vix launcher: `D:\Vix\start-vix.bat`
- Vix agent prompt (source): `D:\Vix\vix-general.md`
- Vix agent prompt (live): `~/.vix/agents/general.md` (WSL)
- Vix desktop shortcut: `C:\Users\click\Desktop\Vix.lnk`
- Qwen config: `C:\Users\click\.qwen\settings.json`
- Master API keys: `D:\Shared\MASTER_API_KEYS.env`
- Obsidian vault: `D:\Obsidian`
- CPR skills: `C:\Users\click\.claude\commands\`
