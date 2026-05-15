$desktop = [System.Environment]::GetFolderPath('Desktop')
$shell = New-Object -ComObject WScript.Shell

# Icon sources - using Windows built-in shell32.dll icons by index
# shell32.dll icon indexes: 13=terminal, 77=lock, 22=search, 269=tools, 44=network
$agents = @(
    @{ Name="Recon"; Dir="D:\Recon";  IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=23  },  # magnifier/search
    @{ Name="Pwn";   Dir="D:\Pwn";    IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=77  },  # lock/key
    @{ Name="Crypt"; Dir="D:\Crypt";  IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=167 },  # padlock
    @{ Name="SICS";  Dir="D:\SICS";   IconPath="%SystemRoot%\System32\shell32.dll"; IconIdx=269 }   # wrench/tools
)

$models = @("laguna", "ring-2.6", "owl")

foreach ($agent in $agents) {
    foreach ($model in $models) {
        $batPath = "$($agent.Dir)\start-$model.bat"
        $lnkPath = "$desktop\$($agent.Name)-$model.lnk"
        $lnk = $shell.CreateShortcut($lnkPath)
        $lnk.TargetPath = $batPath
        $lnk.WorkingDirectory = $agent.Dir
        $lnk.WindowStyle = 1
        $lnk.IconLocation = "$($agent.IconPath),$($agent.IconIdx)"
        $lnk.Save()
        Write-Host "Created: $($agent.Name)-$model.lnk"
    }
}

# Master launcher - use a different icon (command prompt style)
$lnk = $shell.CreateShortcut("$desktop\CTF-Team.lnk")
$lnk.TargetPath = "D:\Olympus\start-ctf-team.bat"
$lnk.WorkingDirectory = "D:\Olympus"
$lnk.WindowStyle = 1
$lnk.IconLocation = "%SystemRoot%\System32\shell32.dll,44"
$lnk.Save()
Write-Host "Created: CTF-Team.lnk (master launcher)"

Write-Host ""
Write-Host "Done. 13 shortcuts created with icons."
Write-Host "Move them into your CTF desktop folder."
