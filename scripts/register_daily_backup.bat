@echo off
:: Run as Administrator
:: To change the time, edit the -At "17:00" line below

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NonInteractive -ExecutionPolicy Bypass -File D:\Olympus\scripts\daily_backup.ps1';" ^
  "$trigger = New-ScheduledTaskTrigger -Daily -At '17:00';" ^
  "$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2) -MultipleInstances IgnoreNew;" ^
  "$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -RunLevel Highest;" ^
  "Register-ScheduledTask -TaskName 'OlympusDailyBackup' -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force"

echo Done. Backup scheduled for 5:00 PM daily. Will catch up if PC was off.
pause
