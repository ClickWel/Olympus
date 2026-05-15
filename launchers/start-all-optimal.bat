@echo off
echo Launching optimal models for all agents...
echo.

echo Starting Crypt - Laguna (reasoning)...
start "Crypt" cmd /k "D:\Crypt\start-laguna.bat"

timeout /t 2 /nobreak >nul

echo Starting Pwn - GPT OSS 20B (tool calling)...
start "Pwn" cmd /k "D:\Pwn\start-oss20b.bat"

timeout /t 2 /nobreak >nul

echo Starting Recon - Gemini 3 (speed)...
start "Recon" cmd /k "D:\Recon\start-gemini3.bat"

timeout /t 2 /nobreak >nul

echo Starting SICS - Laguna (general)...
start "SICS" cmd /k "D:\SICS\start-laguna.bat"

echo.
echo All agents launched with optimal models.