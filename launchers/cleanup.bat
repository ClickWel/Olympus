@echo off
title Olympus Cleanup
color 0A
echo.
echo [OLYMPUS CLEANUP] Killing orphaned processes and flushing VRAM...
echo.

REM --- Kill all ollama processes ---
echo Stopping ollama...
taskkill /F /IM ollama.exe /T >nul 2>&1
timeout /t 1 /nobreak >nul

REM --- Kill stale node/node20 processes older than 1 hour ---
echo Killing stale node processes...
powershell -ExecutionPolicy Bypass -Command ^
  "Get-Process -Name 'node','node20' -ErrorAction SilentlyContinue | Where-Object { $_.StartTime -lt (Get-Date).AddHours(-1) } | ForEach-Object { Write-Host \"  Killed: $($_.Name) PID $($_.Id) (started $($_.StartTime))\"; Stop-Process -Id $_.Id -Force }"

REM --- Restart ollama so it's ready ---
echo.
echo Restarting ollama...
start "" "C:\Users\click\AppData\Local\Programs\Ollama\ollama app.exe"
timeout /t 3 /nobreak >nul

REM --- Evict any loaded models from VRAM ---
echo Flushing VRAM...
powershell -ExecutionPolicy Bypass -Command ^
  "try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/ps' -Method GET -TimeoutSec 5; foreach ($m in $r.models) { $b = '{\"model\": \"' + $m.name + '\", \"keep_alive\": \"0\"}'; Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/generate' -Method POST -Body $b -ContentType 'application/json' -TimeoutSec 10 | Out-Null; Write-Host \"  Evicted: $($m.name)\" } } catch { Write-Host '  Nothing to evict or ollama not ready yet' }"

REM --- Report RAM ---
echo.
echo RAM status:
powershell -ExecutionPolicy Bypass -Command ^
  "$os = Get-WmiObject Win32_OperatingSystem; $free = [int]($os.FreePhysicalMemory/1MB); $total = [int]($os.TotalVisibleMemorySize/1MB); $used = $total - $free; Write-Host \"  Used: ${used}GB / Free: ${free}GB / Total: ${total}GB\""

echo.
echo [DONE] System cleaned up. Launch Talos or any model fresh.
echo.
pause
