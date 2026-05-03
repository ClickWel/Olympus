$WshShell = New-Object -ComObject WScript.Shell
$desktop = [System.Environment]::GetFolderPath("Desktop")

# kill-brave-debug shortcut
$shortcut1 = $WshShell.CreateShortcut("$desktop\kill-brave-debug.lnk")
$shortcut1.TargetPath = "D:\Olympus\scripts\kill-brave-debug.bat"
$shortcut1.WorkingDirectory = "D:\Olympus\scripts"
$shortcut1.Description = "Kill Brave Remote Debug Port"
$shortcut1.IconLocation = "C:\Windows\System32\shell32.dll,131"
$shortcut1.Save()

# process-report shortcut
$shortcut2 = $WshShell.CreateShortcut("$desktop\process-report.lnk")
$shortcut2.TargetPath = "D:\Olympus\scripts\process-report.bat"
$shortcut2.WorkingDirectory = "D:\Olympus\scripts"
$shortcut2.Description = "Run Olympus Process Monitor Report"
$shortcut2.IconLocation = "C:\Windows\System32\shell32.dll,21"
$shortcut2.Save()

Write-Host "Shortcuts created on desktop. Right-click either one > Properties > Change Icon to customize."
