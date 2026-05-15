$pairs = @(
    "D:\Olympus\opencode\CLAUDE.md|D:\Olympus\CLAUDE.md",
    "D:\Atlas\opencode\CLAUDE.md|D:\Atlas\CLAUDE.md",
    "D:\Atlas\opencode\AGENTS.md|D:\Atlas\AGENTS.md",
    "D:\Argus\opencode\CLAUDE.md|D:\Argus\CLAUDE.md",
    "D:\Argus\opencode\AGENTS.md|D:\Argus\AGENTS.md",
    "D:\Talos\opencode\AGENTS.md|D:\Talos\AGENTS.md"
)

foreach ($entry in $pairs) {
    $parts = $entry -split '\|'
    $link = $parts[0]
    $target = $parts[1]
    if (Test-Path $link) { Remove-Item $link -Force }
    New-Item -ItemType SymbolicLink -Path $link -Target $target | Out-Null
    $item = Get-Item $link
    Write-Host "$($item.FullName) -> $($item.Target) [LinkType: $($item.LinkType)]"
}
