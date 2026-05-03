@echo off
:: Run as Administrator
:: Schedules a full Windows system image backup to F: every Sunday at 3:00 AM
:: PC will wake from sleep to run it, then return to sleep

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$action = New-ScheduledTaskAction -Execute 'wbadmin.exe' -Argument 'start backup -backupTarget:F: -include:C: -allCritical -quiet';" ^
  "$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At '03:00';" ^
  "$settings = New-ScheduledTaskSettingsSet -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Hours 3) -MultipleInstances IgnoreNew;" ^
  "$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -RunLevel Highest;" ^
  "Register-ScheduledTask -TaskName 'OlympusWeeklySystemImage' -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force"

echo Done. System image backup scheduled for every Sunday at 3:00 AM.
echo PC will wake from sleep to run it.
pause
