@echo off
echo Launching Hermes (Talos profile) with qwen3-6 alias (qwen/qwen3.6-plus via LM Studio)...
echo Make sure LM Studio is running with qwen3.6-plus loaded on http://10.0.0.25:1234
echo.
wsl.exe -e bash -c "cd ~ && hermes --profile talos /model qwen3-6"
pause
