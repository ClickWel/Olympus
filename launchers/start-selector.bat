@echo off
echo ================================
echo  Olympus Model Selector
echo ================================
echo.
echo Models:
echo  1. Laguna (reasoning)
echo  2. GPT OSS 20B (tool calling)
echo  3. Gemini 3 (speed)
echo  4. Ring 2.6 (deep reasoning)
echo  5. Owl (legacy)
echo.
choice /c 12345 /n /m "Select model (1-5): "

if errorlevel 5 goto SET_MODEL5
if errorlevel 4 goto SET_MODEL4
if errorlevel 3 goto SET_MODEL3
if errorlevel 2 goto SET_MODEL2
goto SET_MODEL1

:SET_MODEL1
set MODEL=poolside/laguna-m.1:free
set PROVIDER=openrouter
goto DIR_SELECT
:SET_MODEL2
set MODEL=openai/gpt-oss-20b:free
set PROVIDER=openrouter
goto DIR_SELECT
:SET_MODEL3
set MODEL=gemini-3-flash-preview
set PROVIDER=google
goto DIR_SELECT
:SET_MODEL4
set MODEL=inclusionai/ring-2.6-1t:free
set PROVIDER=openrouter
goto DIR_SELECT
:SET_MODEL5
set MODEL=openrouter/owl-alpha
set PROVIDER=openrouter
goto DIR_SELECT
echo.
echo Directories:
echo  1. D:\Crypt
echo  2. D:\Pwn
echo  3. D:\Recon
echo  4. D:\SICS
echo  5. D:\Olympus (default)
echo.
choice /c 12345 /n /m "Select directory (1-5): "

if errorlevel 5 set DIR=D:\Olympus
if errorlevel 4 set DIR=D:\SICS
if errorlevel 3 set DIR=D:\Recon
if errorlevel 2 set DIR=D:\Pwn
if errorlevel 1 set DIR=D:\Crypt

if "%PROVIDER%"=="google" goto LAUNCH_GOOGLE
goto LAUNCH_OPENROUTER

:LAUNCH_OPENROUTER
call D:\Olympus\scripts\claude-code-windows-shell.bat
for /f "tokens=2 delims==" %%A in ('findstr /i "^OPENROUTER_API_KEY=" "D:\Shared\MASTER_API_KEYS.env"') do set ANTHROPIC_AUTH_TOKEN=%%A
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=https://openrouter.ai/api
set ANTHROPIC_MODEL=%MODEL%
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "%MODEL%" --startingDirectory "%DIR%" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
goto :eof

:LAUNCH_GOOGLE
call D:\Olympus\scripts\claude-code-windows-shell.bat
for /f "tokens=2 delims==" %%A in ('findstr /i "^GOOGLE_GENERATIVE_AI_API_KEY=" "D:\Shared\MASTER_API_KEYS.env"') do set ANTHROPIC_AUTH_TOKEN=%%A
set ANTHROPIC_API_KEY=
set ANTHROPIC_BASE_URL=https://generativelanguage.googleapis.com/v1beta
set ANTHROPIC_MODEL=%MODEL%
set CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "%MODEL%" --startingDirectory "%DIR%" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
goto :eof