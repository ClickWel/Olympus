@echo off
"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe" -w new new-tab --title "phi4 [Pi]" --tabColor "#8B4513" --startingDirectory "D:\Talos" -- cmd /k node "C:\Users\click\AppData\Roaming\npm\node_modules\@mariozechner\pi-coding-agent\dist\cli.js" --provider ollama --model phi4 --no-tools
