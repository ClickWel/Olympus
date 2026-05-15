@echo off
start /min "" "D:\Crypt\start-ring-2.6.bat"
timeout /t 1 /nobreak >nul
start /min "" "D:\Pwn\start-ring-2.6.bat"
timeout /t 1 /nobreak >nul
start /min "" "D:\Recon\start-ring-2.6.bat"
timeout /t 1 /nobreak >nul
start /min "" "D:\SICS\start-ring-2.6.bat"
