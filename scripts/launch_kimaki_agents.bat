@echo off
REM Launch Atlas, Argus, and Talos Kimaki instances in separate Windows Terminal tabs.
REM Olympus is assumed to already be running.

wt --title "Kimaki-Atlas" cmd /k "set \"KIMAKI_LOCK_PORT=31001\" && set \"KIMAKI_BOT_TOKEN=***REMOVED***R-PzFr7XzbdEkUNuVFBYi_kYUMxptcpFPsM\" && npx -y kimaki@latest --data-dir %USERPROFILE%\.kimaki-atlas" ; ^
new-tab --title "Kimaki-Argus" cmd /k "set \"KIMAKI_LOCK_PORT=31002\" && set \"KIMAKI_BOT_TOKEN=***REMOVED***j.F-t9sI6g9mH1C23_HuUB6q8g8B1PDd53O6O_vM\" && npx -y kimaki@latest --data-dir %USERPROFILE%\.kimaki-argus" ; ^
new-tab --title "Kimaki-Talos" cmd /k "set \"KIMAKI_LOCK_PORT=31003\" && set \"KIMAKI_BOT_TOKEN=***REMOVED***B.pcUMVDMN3v7GoDKcPI-6XkbWtgLA3XcUbIzM7o\" && npx -y kimaki@latest --data-dir %USERPROFILE%\.kimaki-talos"
