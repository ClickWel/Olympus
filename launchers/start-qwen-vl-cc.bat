@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
set ANTHROPIC_BASE_URL=http://localhost:1234
set ANTHROPIC_AUTH_TOKEN=lmstudio
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Qwen VL" --tabColor "#2D4A6A" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe --model mradermacherqwen2.5vl-7b-instruct-i1"
