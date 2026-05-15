$ws = New-Object -COM WScript.Shell
$s = $ws.CreateShortcut("$env:USERPROFILE\Desktop\Kimaki.lnk")
$s.TargetPath = "D:\Olympus\scripts\start-kimaki.bat"
$s.WorkingDirectory = "$env:USERPROFILE\.kimaki"
$s.Save()
Write-Output "Shortcut created."
