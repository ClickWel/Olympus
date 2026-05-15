@echo off
REM Launch all 4 Kimaki agent bots in one Windows Terminal window.
REM Close the window to take all agents offline.

set WT="C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_1.24.10921.0_x64__8wekyb3d8bbwe\wt.exe"

%WT% --title "Collab" cmd /k "set \"KIMAKI_BOT_TOKEN=***REMOVED***-roe_wt4Y\" && npx -y kimaki@latest --data-dir %%USERPROFILE%%\.kimaki" ^
  ; new-tab --title "Atlas" cmd /k "set \"KIMAKI_LOCK_PORT=31001\" && set \"KIMAKI_BOT_TOKEN=***REMOVED***R-PzFr7XzbdEkUNuVFBYi_kYUMxptcpFPsM\" && npx -y kimaki@latest --data-dir %%USERPROFILE%%\.kimaki-atlas" ^
  ; new-tab --title "Argus" cmd /k "set \"KIMAKI_LOCK_PORT=31002\" && set \"KIMAKI_BOT_TOKEN=***REMOVED***j.F-t9sI6g9mH1C23_HuUB6q8g8B1PDd53O6O_vM\" && npx -y kimaki@latest --data-dir %%USERPROFILE%%\.kimaki-argus" ^
  ; new-tab --title "Talos" cmd /k "set \"KIMAKI_LOCK_PORT=31003\" && set \"KIMAKI_BOT_TOKEN=***REMOVED***B.pcUMVDMN3v7GoDKcPI-6XkbWtgLA3XcUbIzM7o\" && npx -y kimaki@latest --data-dir %%USERPROFILE%%\.kimaki-talos"
