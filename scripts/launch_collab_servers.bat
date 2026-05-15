@echo off
echo Starting collab servers...

REM Start opencode serve from each agent's opencode subfolder (has correct model + skills config + identity files)
set OPENROUTER_API_KEY=***REMOVED***
start "collab-olympus" /MIN cmd /c "cd /d D:\Olympus\opencode && D:\OpenCode\opencode-cli.exe serve --port 54001 --print-logs > D:\Olympus\opencode\serve.log 2>&1"
start "collab-atlas"   /MIN cmd /c "cd /d D:\Atlas\opencode   && D:\OpenCode\opencode-cli.exe serve --port 54002 --print-logs > D:\Atlas\opencode\serve.log 2>&1"
start "collab-argus"   /MIN cmd /c "cd /d D:\Argus\opencode   && D:\OpenCode\opencode-cli.exe serve --port 54003 --print-logs > D:\Argus\opencode\serve.log 2>&1"
start "collab-talos"   /MIN cmd /c "cd /d D:\Talos\opencode   && D:\OpenCode\opencode-cli.exe serve --port 54004 --print-logs > D:\Talos\opencode\serve.log 2>&1"

echo Waiting for servers to start...
timeout /t 3 /nobreak >nul

REM Start the Discord watcher in a visible window
start "collab-watcher" cmd /k "python D:\Shared\discord_collab_watcher.py"

echo.
echo Collab servers running:
echo   Olympus : http://127.0.0.1:54001
echo   Atlas   : http://127.0.0.1:54002
echo   Argus   : http://127.0.0.1:54003
echo   Talos   : http://127.0.0.1:54004
echo   Watcher : watching Discord for pings
echo.
echo Run stop_collab_servers.bat to shut everything down.
