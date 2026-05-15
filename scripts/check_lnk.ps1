$shell = New-Object -ComObject WScript.Shell
$a = $shell.CreateShortcut('C:\Users\click\Desktop\Atlas OC.lnk')
$t = $shell.CreateShortcut('C:\Users\click\Desktop\Talos OC.lnk')
Write-Output $a.TargetPath
Write-Output $t.TargetPath
