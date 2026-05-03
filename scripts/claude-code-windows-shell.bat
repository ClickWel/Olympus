@echo off
rem Force Windows Claude Code launchers to prefer PowerShell even if Git Bash
rem or WSL exported a Unix SHELL value into the parent environment.
set "SHELL=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
set "CLAUDE_CODE_SHELL=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
set "ComSpec=%SystemRoot%\System32\cmd.exe"
exit /b 0
