@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
set ANTHROPIC_BASE_URL=http://localhost:1234
set ANTHROPIC_AUTH_TOKEN=lmstudio
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "OmniClaw" --tabColor "#6A2D6A" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe --model omniclaw-qwen3.5-9b-claude-4.6-opus-uncensored-v2"
