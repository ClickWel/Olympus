@echo off
call D:\Olympus\scripts\claude-code-windows-shell.bat
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "Olympus" --tabColor "#2D6A2D" --startingDirectory "D:\Olympus" -- cmd /k "%USERPROFILE%\.local\bin\claude.exe"
