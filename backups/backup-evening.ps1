$backupDir = "D:\Olympus\backups\2026-04-08_evening"
if (-not (Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir | Out-Null }

Copy-Item "D:\Olympus\AGENTS.md" "$backupDir\AGENTS.md.olympus"
Copy-Item "D:\Argus\AGENTS.md" "$backupDir\AGENTS.md.argus"
Copy-Item "D:\Atlas\AGENTS.md" "$backupDir\AGENTS.md.atlas"
Copy-Item "D:\Olympus\sessions\2026-04-08.md" "$backupDir\session-2026-04-08.md"
Copy-Item "D:\Olympus\memory\MEMORY.md" "$backupDir\MEMORY.md"
Copy-Item "D:\Olympus\vision\analyze-image.ps1" "$backupDir\vision-tool.ps1"
Copy-Item "C:\Users\click\.config\opencode\opencode.json" "$backupDir\opencode.json"
Copy-Item "D:\Olympus\sessions\2026-04-08.md" "$backupDir\session-2026-04-08.md"

Write-Host "Backed up to: $backupDir"
Get-ChildItem $backupDir | Select-Object Name
