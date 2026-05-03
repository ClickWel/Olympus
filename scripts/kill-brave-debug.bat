@echo off
title Kill Brave Debug Port
echo Killing Brave debug port :9222...

REM Find and kill the process listening on 9222
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":9222" ^| findstr "LISTENING"') do (
    echo Found listener PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

REM Also kill any Brave instances launched with remote-debugging flags
wmic process where "Name='brave.exe' and CommandLine like '%%remote-debugging-port%%'" delete >nul 2>&1

echo Done. Brave debug port closed.
echo %DATE% %TIME% - kill-brave-debug.bat executed >> "D:\Shared\reports\brave_debug_kill_log.txt"
timeout /t 3
