@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
set ANTHROPIC_BASE_URL=http://localhost:1234
set ANTHROPIC_AUTH_TOKEN=lmstudio
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "i1" --tabColor "#B8860B" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe --model qwen3.5-9b-glm5.1-distill-v1-i1"
