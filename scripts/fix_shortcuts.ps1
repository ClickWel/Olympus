$shell = New-Object -ComObject WScript.Shell

$s1 = $shell.CreateShortcut('C:\Users\click\Desktop\Start Collab.lnk')
$s1.TargetPath = 'D:\Olympus\scripts\launch_collab_servers.bat'
$s1.WorkingDirectory = 'D:\Olympus\scripts'
$s1.Save()

$s2 = $shell.CreateShortcut('C:\Users\click\Desktop\Stop Collab.lnk')
$s2.TargetPath = 'D:\Olympus\scripts\stop_collab_servers.bat'
$s2.WorkingDirectory = 'D:\Olympus\scripts'
$s2.Save()

Write-Output 'Done'
