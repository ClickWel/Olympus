@echo off
echo Switching Claude Code to SUBSCRIPTION mode...
python "%~dp0scripts\cc_toggle_auth.py" subscription
echo.
pause
