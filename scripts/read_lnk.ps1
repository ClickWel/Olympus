$sh = New-Object -ComObject WScript.Shell
$lnk = $sh.CreateShortcut('C:\Users\click\Desktop\Hack Session.lnk')
Write-Host "Target:" $lnk.TargetPath
Write-Host "Args:" $lnk.Arguments
Write-Host "WorkDir:" $lnk.WorkingDirectory
