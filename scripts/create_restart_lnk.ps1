$ws = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut("C:\Users\click\Desktop\RESTART HERMES.lnk")
$lnk.TargetPath = "D:\Olympus\scripts\restart-hermes.bat"
$lnk.WorkingDirectory = "D:\Olympus\scripts"
$lnk.WindowStyle = 7
$lnk.IconLocation = "C:\Windows\System32\shell32.dll,238"
$lnk.Description = "Restart Hermes Agent"
$lnk.Save()
Write-Host "Done - RESTART HERMES.lnk created"
