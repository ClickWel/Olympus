@echo off
wsl bash -ic "pgrep -f '/bin/hermes$' | xargs kill 2>/dev/null" 2>nul
exit
