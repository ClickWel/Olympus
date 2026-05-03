@echo off
for /f "tokens=1,* delims==" %%A in ('findstr /v "^#" "D:\Hermes\config\MASTER_API_KEYS.env"') do (
    if not "%%A"=="" if not "%%B"=="" set "%%A=%%B"
)
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Google Gemini (OpenCode)" --tabColor "#4285f4" --startingDirectory "D:\Olympus" -- cmd /k "cd /d D:\OpenCode && opencode-cli.exe"
