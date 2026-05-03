$os = Get-CimInstance Win32_OperatingSystem
$ram_total = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$ram_free = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
$ram_used = [math]::Round($ram_total - $ram_free, 1)
$ram_pct = [math]::Round($ram_used / $ram_total * 100)
Write-Host "=== RAM ==="
Write-Host "Used: $ram_used GB / $ram_total GB ($ram_pct%)"
Write-Host ""

Write-Host "=== DISK ==="
Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 } | ForEach-Object {
    $free = [math]::Round($_.FreeSpace / 1GB, 1)
    $total = [math]::Round($_.Size / 1GB, 1)
    $used = [math]::Round($total - $free, 1)
    $pct = [math]::Round($used / $total * 100)
    Write-Host "$($_.DeviceID) $used GB used / $total GB total ($pct% full) - $($_.VolumeName)"
}
Write-Host ""

Write-Host "=== TOP PROCESSES BY RAM ==="
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 20 | ForEach-Object {
    $ram = [math]::Round($_.WorkingSet / 1MB)
    Write-Host "$($_.Name.PadRight(30)) RAM: $ram MB"
}
Write-Host ""

Write-Host "=== GPU (VRAM) ==="
try {
    $gpu = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
    Write-Host "GPU: $($gpu.Name)"
    Write-Host "Driver: $($gpu.DriverVersion)"
} catch {
    Write-Host "GPU query failed"
}
Write-Host ""

Write-Host "=== OLLAMA LOADED MODELS ==="
& ollama ps 2>&1
