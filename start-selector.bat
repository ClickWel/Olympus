@echo off
echo ================================
echo  Olympus Model Selector
echo ================================
echo  1. Laguna M.1 (OpenRouter - default)
echo  2. Claude Sonnet 4 (GitHub Models - via proxy)
echo  3. GPT-5 (GitHub Models - OpenAI client)
echo ================================
choice /c 123 /n /m "Choice (1-3): "

if errorlevel 3 goto GPT
if errorlevel 2 goto CLAUDE
goto LAGUNA

:LAGUNA
call D:\Olympus\scripts\claude-code-windows-shell.bat
for /f "tokens=2 delims==" %%A in ('findstr /i "^OPENROUTER_API_KEY=" "D:\Shared\MASTER_API_KEYS.env"') do set ANTHROPIC_AUTH_TOKEN=%%A
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=https://openrouter.ai/api
set ANTHROPIC_MODEL=poolside/laguna-m.1:free
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Laguna M.1 (OpenRouter)" --tabColor "#0066CC" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
goto :eof

:CLAUDE
call D:\Olympus\scripts\claude-code-windows-shell.bat
for /f "tokens=2 delims==" %%A in ('findstr /i "^GITHUB_MODELS_API_KEY=" "D:\Hermes\config\MASTER_API_KEYS.env"') do set ANTHROPIC_AUTH_TOKEN=%%A
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=http://localhost:8080
set ANTHROPIC_MODEL=claude-sonnet-4
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
echo Starting GitHub Models proxy for Claude...
start "Claude Proxy" cmd /k "python D:\Olympus\scripts\github_models_proxy.py"
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Claude Sonnet 4 (GitHub)" --tabColor "#00CC66" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
goto :eof

:GPT
for /f "tokens=2 delims==" %%A in ('findstr /i "^GITHUB_MODELS_API_KEY=" "D:\Hermes\config\MASTER_API_KEYS.env"') do set GITHUB_TOKEN=%%A
echo.
echo GitHub Models API - GPT-5
echo Endpoint: https://models.github.ai/inference/chat/completions
echo Model: openai/gpt-5
echo.
echo Paste this into Python:
echo.
echo from openai import OpenAI
echo client = OpenAI(base_url="https://models.github.ai/inference", api_key="%GITHUB_TOKEN%")
echo r = client.chat.completions.create(model="openai/gpt-5", messages=[{"role":"user","content":"Hello"}], extra_headers={"X-GitHub-Api-Version":"2026-03-10"})
echo print(r.choices[0].message.content)
echo.
cmd /k
goto :eof
