@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
set ANTHROPIC_AUTH_TOKEN= unused-but-required
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=http://127.0.0.1:8082
set ANTHROPIC_MODEL=gemini-2.0-flash
set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
wscript "D:\Olympus\start-google-proxy.vbs"
timeout /t 3 /nobreak >nul
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Google Gemini" --tabColor "#4285f4" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
