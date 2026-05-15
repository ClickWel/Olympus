@echo off
start "" python "D:\Olympus\scripts\gemini_proxy.py"
timeout /t 2 /nobreak >nul
set ANTHROPIC_AUTH_TOKEN=dummy
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=http://localhost:4444
set ANTHROPIC_MODEL=google/gemini-2.5-flash-latest:free
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Gemini 2.5 Flash (Free)" --tabColor "#1A73E8" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
