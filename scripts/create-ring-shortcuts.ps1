$desktop = [System.Environment]::GetFolderPath('Desktop')
$shell = New-Object -ComObject WScript.Shell

$agents = @(
    @{ Name="Crypt"; Dir="D:\Crypt";  IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=167 },
    @{ Name="Pwn";   Dir="D:\Pwn";    IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=77  },
    @{ Name="Recon"; Dir="D:\Recon";  IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=23  },
    @{ Name="SICS";  Dir="D:\SICS";   IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=269 }
)

# CTF shortcuts
foreach ($agent in $agents) {
    $batPath = "$($agent.Dir)\start-ring-2.6.bat"
    $lnkPath = "$desktop\$($agent.Name)-ring-2.6.lnk"
    $lnk = $shell.CreateShortcut($lnkPath)
    $lnk.TargetPath = $batPath
    $lnk.WorkingDirectory = $agent.Dir
    $lnk.WindowStyle = 1
    $lnk.IconLocation = "$($agent.IconPath),$($agent.IconIdx)"
    $lnk.Save()
    Write-Host "Created: $($agent.Name)-ring-2.6.lnk"
}

# BB shortcuts
foreach ($agent in $agents) {
    $batPath = "$($agent.Dir)\start-ring-2.6-bb.bat"
    $lnkPath = "$desktop\$($agent.Name)-ring-2.6-bb.lnk"
    $lnk = $shell.CreateShortcut($lnkPath)
    $lnk.TargetPath = $batPath
    $lnk.WorkingDirectory = "$($agent.Dir)\bb"
    $lnk.WindowStyle = 1
    $lnk.IconLocation = "$($agent.IconPath),$($agent.IconIdx)"
    $lnk.Save()
    Write-Host "Created: $($agent.Name)-ring-2.6-bb.lnk"
}

Write-Host ""
Write-Host "Done. 8 shortcuts created."
