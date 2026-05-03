$ws = New-Object -ComObject WScript.Shell
$launch = $ws.CreateShortcut("C:\Users\click\Desktop\LAUNCH HERMES.lnk")
$close = $ws.CreateShortcut("C:\Users\click\Desktop\CLOSE HERMES.lnk")
Write-Host ("LAUNCH target: " + $launch.TargetPath)
Write-Host ("LAUNCH exists: " + (Test-Path $launch.TargetPath))
Write-Host ("CLOSE target: " + $close.TargetPath)
Write-Host ("CLOSE exists: " + (Test-Path $close.TargetPath))
