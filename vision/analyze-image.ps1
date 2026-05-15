param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath
)

# Extract ScreenShot filename - OpenCode passes paths like "C:/Git/vision Screenshot 2026-04-28 232425.png"
if ($ImagePath -match "Screenshot (\d{4}-\d{2}-\d{2} \d{6}\.png)") {
    $fileName = "Screenshot " + $matches[1]
} elseif ($ImagePath -match "([^\s]+\.png)") {
    $fileName = $matches[1]
} else {
    $fileName = Split-Path $ImagePath -Leaf
}

# Search in common directories + all drives
$searchDirs = @("D:\Shared", "D:\Olympus", "D:\Atlas", "D:\Clawdbot", "D:\Cerberus", "D:\Talos", "C:\Users\click\Desktop", "C:\Users\click\Pictures", "D:\Shared\reports")

$resolvedPath = $null
foreach ($dir in $searchDirs) {
    $candidate = Join-Path $dir $fileName
    if (Test-Path $candidate) {
        $resolvedPath = $candidate
        break
    }
}

if (-not $resolvedPath) {
    Write-Output "Error: Image not found - looking for $fileName"
    exit 1
}

# Run vision bridge
$python = "python"
$result = & $python "D:/Olympus/skills/vision_bridge.py" --path "$resolvedPath" --nvidia 2>&1

Write-Output $result