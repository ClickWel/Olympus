@echo off
rem Kill any stale Python audio processes that may be holding the mic
wsl bash -ic "pkill -f 'sounddevice\|sd\.rec\|voice_mode' 2>/dev/null; true" 2>nul

rem PulseAudio is started hidden by launch_hermes_invisble.vbs via start-pulse.bat

start "" wscript.exe "D:\Hermes\launch_hermes_invisble.vbs"
