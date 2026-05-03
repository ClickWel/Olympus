@echo off
echo Launching OpenCode CLI with Qwen3.5-9B via llama.cpp...
echo Make sure start-qwen.bat is running on http://10.0.0.25:8085
echo.
cd /d D:\OpenCode
"D:\Talos\bin\opencode.exe" --model llamacpp/Qwen3.5-9B.Q4_K_M.gguf
pause
