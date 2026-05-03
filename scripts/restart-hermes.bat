@echo off
rem Kill Hermes and any stale Python audio processes
wsl bash -ic "pgrep -f '/bin/hermes$' | xargs kill 2>/dev/null; pkill -f 'sounddevice\|sd\.rec\|voice_mode' 2>/dev/null; true" 2>nul
timeout /t 2 /nobreak >nul

rem Restart PulseAudio fresh so the Windows mic is available
taskkill /IM pulseaudio.exe /F >nul 2>&1
timeout /t 1 /nobreak >nul
start "" /B "D:\PulseAudio\pulseaudio\bin\pulseaudio.exe" --exit-idle-time=-1 -F "D:\PulseAudio\pulseaudio\etc\pulse\default.pa"
timeout /t 2 /nobreak >nul

start "" wscript.exe "D:\Hermes\launch_hermes_invisble.vbs"
exit
