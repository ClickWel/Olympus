Write-Host "=== CMD PROCESS DETAILS ==="
$proc = Get-Process -Id 23920 -ErrorAction SilentlyContinue
if ($proc) {
    Write-Host "Name: $($proc.Name)"
    Write-Host "PID: $($proc.Id)"
    Write-Host "Started: $($proc.StartTime)"
    Write-Host "CPU total: $($proc.CPU) seconds"
    Write-Host "RAM: $([math]::Round($proc.WorkingSet/1MB)) MB"

    $wmi = Get-CimInstance Win32_Process -Filter "ProcessId = 23920" -ErrorAction SilentlyContinue
    if ($wmi) {
        Write-Host "Command line: $($wmi.CommandLine)"
        Write-Host "Parent PID: $($wmi.ParentProcessId)"
        $parent = Get-Process -Id $wmi.ParentProcessId -ErrorAction SilentlyContinue
        if ($parent) { Write-Host "Parent name: $($parent.Name)" }
    }
} else {
    Write-Host "Process 23920 no longer running"
}

Write-Host ""
Write-Host "=== ALL CMD PROCESSES ==="
Get-CimInstance Win32_Process -Filter "Name = 'cmd.exe'" | Select-Object ProcessId, ParentProcessId, CommandLine | Format-List
