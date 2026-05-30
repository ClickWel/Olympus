@echo off
rem Force Windows Claude Code launchers to prefer PowerShell even if Git Bash
rem or WSL exported a Unix SHELL value into the parent environment.
set "SHELL=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
set "CLAUDE_CODE_SHELL=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
set "ComSpec=%SystemRoot%\System32\cmd.exe"
rem Clear any OpenRouter/provider overrides that may have leaked from a hack team window
set "ANTHROPIC_BASE_URL="
set "ANTHROPIC_MODEL="
set "ANTHROPIC_AUTH_TOKEN="
exit /b 0
