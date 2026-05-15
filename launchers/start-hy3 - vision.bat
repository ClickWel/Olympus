@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
for /f "tokens=2 delims==" %%A in ('findstr /i "^OPENROUTER_API_KEY=" "D:\Shared\MASTER_API_KEYS.env"') do set ANTHROPIC_AUTH_TOKEN=%%A
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=https://openrouter.ai/api
set ANTHROPIC_MODEL=baidu/qianfan-ocr-fast:free
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "HY3 + Vision" --tabColor "#cc00a0" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
