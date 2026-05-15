@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
for /f "tokens=2 delims==" %%A in ('findstr /i "^GITHUB_MODELS_API_KEY=" "D:\Shared\MASTER_API_KEYS.env"') do set ANTHROPIC_AUTH_TOKEN=%%A
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=https://models.github.ai/inference
set ANTHROPIC_MODEL=openai/gpt-4o
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "GPT-4O" --tabColor "#0066CC" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
