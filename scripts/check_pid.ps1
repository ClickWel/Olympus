Write-Host "=== PARENT PROCESS (10412) ==="
$parent = Get-Process -Id 10412 -ErrorAction SilentlyContinue
if ($parent) {
    Write-Host "Name: $($parent.Name)"
    Write-Host "PID: $($parent.Id)"
    Write-Host "Started: $($parent.StartTime)"
    Write-Host "CPU total: $($parent.CPU) seconds"
    Write-Host "RAM: $([math]::Round($parent.WorkingSet/1MB)) MB"
    $wmi = Get-CimInstance Win32_Process -Filter "ProcessId = 10412" -ErrorAction SilentlyContinue
    if ($wmi) {
        Write-Host "Command line: $($wmi.CommandLine)"
        Write-Host "Parent PID: $($wmi.ParentProcessId)"
        $gp = Get-Process -Id $wmi.ParentProcessId -ErrorAction SilentlyContinue
        if ($gp) { Write-Host "Grandparent: $($gp.Name) (PID $($gp.Id))" }
    }
} else {
    Write-Host "Process 10412 not found - may have exited"
}

Write-Host ""
Write-Host "=== CHILDREN OF 10412 ==="
Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq 10412 } | Select-Object ProcessId, Name, CommandLine | Format-List

Write-Host ""
Write-Host "=== WHAT IS CMD PID 23920 DOING NOW ==="
$p = Get-CimInstance Win32_Process -Filter "ProcessId = 23920" -ErrorAction SilentlyContinue
if ($p) {
    Write-Host "Still running. Threads: $(($p).ThreadCount)"
    Write-Host "Handle count: $(($p).HandleCount)"
} else {
    Write-Host "No longer running"
}
