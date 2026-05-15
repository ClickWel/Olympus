# sync_to_agents.ps1
# Copies canonical config files from Olympus to Argus, Atlas, and Hermes/Talos.
# Olympus is the single source of truth. Run this after any key/config update.

$olympus = "D:\Olympus"
$agents = @(
    @{Name="Argus"; Dest="D:\Argus\config"},
    @{Name="Atlas"; Dest="D:\Atlas\config"},
    @{Name="Hermes/Talos"; Dest="D:\Hermes\config"}
)

$files = @(
    "MASTER_API_KEYS.env",
    "delegation.md",
    "project_context.md"
)

$log = @()
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$log += "[$ts] sync_to_agents.ps1 started"

foreach ($agent in $agents) {
    $agentName = $agent.Name
    $dest = $agent.Dest
    if (-not (Test-Path $dest)) {
        $log += "  [$agentName] SKIP - path not found: $dest"
        continue
    }
    foreach ($file in $files) {
        $src = Join-Path $olympus $file
        $dst = Join-Path $dest $file
        if (-not (Test-Path $src)) {
            $log += "  [$agentName] SKIP - source missing: $src"
            continue
        }
        try {
            Copy-Item -Path $src -Destination $dst -Force
            $msg = "  [" + $agentName + "] COPIED: " + $file
            $log += $msg
        } catch {
            $msg = "  [" + $agentName + "] ERROR copying " + $file + ": " + $_.Exception.Message
            $log += $msg
        }
    }
}

$ts2 = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$log += "[$ts2] sync_to_agents.ps1 finished"
$log += ""

Write-Output ($log -join "`n")
$logPath = Join-Path $olympus "logs\sync_log.txt"
Add-Content -Path $logPath -Value $log -Encoding UTF8
Write-Output "Log saved to $logPath"
