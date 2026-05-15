@echo off
start /min "" "D:\Recon\start-hy3-bb.bat"
timeout /t 1 /nobreak >nul
start /min "" "D:\SICS\start-hy3-bb.bat"
timeout /t 1 /nobreak >nul
start /min "" "D:\Crypt\start-hy3-bb.bat"
timeout /t 1 /nobreak >nul
start /min "" "D:\Pwn\start-hy3-bb.bat"
