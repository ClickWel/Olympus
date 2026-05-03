@echo off
echo Switching Claude Code to API KEY mode...
python "%~dp0scripts\cc_toggle_auth.py" api
echo.
pause
