$ws = New-Object -COM WScript.Shell
$s = $ws.CreateShortcut("$env:USERPROFILE\Desktop\Stop Kimaki.lnk")
$s.TargetPath = "D:\Olympus\scripts\stop-kimaki.bat"
$s.WorkingDirectory = "$env:USERPROFILE\.kimaki"
$s.Save()
Write-Output "Stop shortcut created."
