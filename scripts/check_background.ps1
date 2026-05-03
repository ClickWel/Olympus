Write-Host "=== RUNNING SCHEDULED TASKS ==="
Get-ScheduledTask | Where-Object { $_.State -eq "Running" } | Select-Object TaskName, TaskPath | Format-Table -AutoSize

Write-Host "=== BACKUP / VSS SERVICES ==="
Get-Service | Where-Object { $_.Status -eq "Running" -and ($_.Name -like "*backup*" -or $_.Name -like "*vss*" -or $_.Name -like "*shadow*" -or $_.Name -like "*wbengine*") } | Select-Object Name, DisplayName | Format-Table -AutoSize

Write-Host "=== DISK ACTIVITY (top IO processes) ==="
Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 10 Name, CPU, Id | Format-Table -AutoSize

Write-Host "=== RECENT WINDOWS BACKUP EVENTS (last 5) ==="
try {
    Get-WinEvent -LogName "Microsoft-Windows-Backup" -MaxEvents 5 -ErrorAction Stop | Select-Object TimeCreated, LevelDisplayName, Message | Format-List
} catch {
    Write-Host "No Windows Backup events found or log not available"
}
