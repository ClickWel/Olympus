@echo off
for /f "tokens=1,* delims==" %%A in ('findstr /v "^#" "D:\Hermes\config\MASTER_API_KEYS.env"') do (
    if not "%%A"=="" if not "%%B"=="" set "%%A=%%B"
)
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Olympus OC" --tabColor "#FFCC00" --startingDirectory "D:\Olympus" -- cmd /k "set OPENAI_API_KEY=%OPENROUTER_API_KEY_OC% && set OPENAI_BASE_URL=%OPENROUTER_ENDPOINT% && set GOOGLE_GENERATIVE_AI_API_KEY=%GOOGLE_GENERATIVE_AI_API_KEY% && set GROQ_API_KEY=%GROQ_API_KEY% && cd /d D:\Olympus && D:\OpenCode\opencode-cli.exe"
