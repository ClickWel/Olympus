@echo off
taskkill /F /IM bun.exe 2>nul
taskkill /F /IM opencode.exe 2>nul
taskkill /F /IM opencode-cli.exe 2>nul
echo Kimaki stopped.
