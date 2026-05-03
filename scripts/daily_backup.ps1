# daily_backup.ps1
# Backs up key folders from C:\Users\click and D:\ to E:\Backups\Daily
# Run via Task Scheduler daily. Logs to E:\Backups\Daily\backup_log.txt

$log = "E:\Backups\Daily\backup_log.txt"
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Ensure the backup root exists before any logging
if (-not (Test-Path "E:\Backups\Daily")) {
    New-Item -ItemType Directory -Path "E:\Backups\Daily" -Force | Out-Null
}

function Write-Log {
    param($msg)
    $line = "[$date] $msg"
    Write-Host $line
    Add-Content -Path $log -Value $line -Encoding UTF8
}

$targets = @(
    # C - user profile
    @{ Src = "C:\Users\click\Documents";   Dst = "E:\Backups\Daily\C\Documents" },
    @{ Src = "C:\Users\click\Desktop";     Dst = "E:\Backups\Daily\C\Desktop" },
    @{ Src = "C:\Users\click\Downloads";   Dst = "E:\Backups\Daily\C\Downloads" },
    @{ Src = "C:\Users\click\.clawdbot-dev"; Dst = "E:\Backups\Daily\C\clawdbot-dev" },
    @{ Src = "C:\Users\click\.atlas-dev";  Dst = "E:\Backups\Daily\C\atlas-dev" },
    @{ Src = "C:\Users\click\.claude";     Dst = "E:\Backups\Daily\C\claude" },

    # D - the team
    @{ Src = "D:\Argus";                   Dst = "E:\Backups\Daily\D\Argus" },
    @{ Src = "D:\Atlas";                   Dst = "E:\Backups\Daily\D\Atlas" },
    @{ Src = "D:\Olympus";                 Dst = "E:\Backups\Daily\D\Olympus" },
    @{ Src = "D:\Cerberus";               Dst = "E:\Backups\Daily\D\Cerberus" },
    @{ Src = "D:\Clawdbot";               Dst = "E:\Backups\Daily\D\Clawdbot" },
    @{ Src = "D:\Clawbot";                Dst = "E:\Backups\Daily\D\Clawbot" },
    @{ Src = "D:\Shared";                 Dst = "E:\Backups\Daily\D\Shared" },

    # D - work
    @{ Src = "D:\Convert_Like_Crazy";     Dst = "E:\Backups\Daily\D\Convert_Like_Crazy" },
    @{ Src = "D:\GITHUB";                 Dst = "E:\Backups\Daily\D\GITHUB" },

    # D - streaming
    @{ Src = "D:\StreamContentPipeline";  Dst = "E:\Backups\Daily\D\StreamContentPipeline" },
    @{ Src = "D:\StreamDeck";             Dst = "E:\Backups\Daily\D\StreamDeck" },
    @{ Src = "D:\VTuber";                 Dst = "E:\Backups\Daily\D\VTuber" },
    @{ Src = "D:\Twitch";                 Dst = "E:\Backups\Daily\D\Twitch" },
    @{ Src = "D:\Twitch Bot";             Dst = "E:\Backups\Daily\D\TwitchBot" },
    @{ Src = "D:\BB Overlay";             Dst = "E:\Backups\Daily\D\BB_Overlay" },
    @{ Src = "D:\Speaker.bot";            Dst = "E:\Backups\Daily\D\Speaker.bot" },
    @{ Src = "D:\Streamer.bot_Resources"; Dst = "E:\Backups\Daily\D\Streamer.bot_Resources" },
    @{ Src = "D:\AI-Backups";             Dst = "E:\Backups\Daily\D\AI-Backups" }
)

Write-Log "--- Backup started ---"

foreach ($t in $targets) {
    if (-not (Test-Path $t.Src)) {
        Write-Log "SKIP (not found): $($t.Src)"
        continue
    }
    Write-Log "Syncing: $($t.Src)"
    $result = robocopy $t.Src $t.Dst /MIR /Z /MT:8 /R:2 /W:5 /NP /NDL /NC /LOG+:$log 2>&1
    if ($LASTEXITCODE -le 3) {
        Write-Log "OK: $($t.Src)"
    } else {
        Write-Log "ERROR (code $LASTEXITCODE): $($t.Src)"
    }
}

Write-Log "--- Backup complete ---"
