@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
for /f "tokens=2 delims==" %%A in ('findstr /i "^OPENROUTER_API_KEY=" "D:\Shared\MASTER_API_KEYS.env"') do set ANTHROPIC_AUTH_TOKEN=%%A
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=https://openrouter.ai/api
set ANTHROPIC_MODEL=z-ai/glm-4.5-air:free
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "GLM 4.5" --tabColor "#7100a6" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
