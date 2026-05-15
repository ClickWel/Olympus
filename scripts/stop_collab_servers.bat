@echo off
echo Stopping collab servers...

taskkill /FI "WINDOWTITLE eq collab-olympus*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq collab-atlas*"   /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq collab-argus*"   /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq collab-talos*"   /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq collab-watcher*" /F >nul 2>&1

REM Also kill any opencode-cli processes on our ports
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":54001 :54002 :54003 :54004"') do taskkill /PID %%a /F >nul 2>&1

echo Collab servers stopped.
