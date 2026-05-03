$imgPath = "C:/Users/click/Desktop/Screenshot 2026-04-08 205328.png"
$base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($imgPath))

Write-Host "=== LOCAL LLAVA 13B ===" -ForegroundColor Cyan
$swLlava = [Diagnostics.Stopwatch]::StartNew()
$body1 = @{
    model = "llava:13b"
    images = @($base64)
    prompt = "Describe this image briefly."
    stream = $false
} | ConvertTo-Json -Depth 10
$null = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -ContentType "application/json" -Body $body1
$swLlava.Stop()
Write-Host "llava:13b: $($swLlava.ElapsedMilliseconds)ms" -ForegroundColor Green

Write-Host ""
Write-Host "=== LOCAL QWEN2.5VL 3B ===" -ForegroundColor Cyan
$swQwen = [Diagnostics.Stopwatch]::StartNew()
$body2 = @{
    model = "qwen2.5vl:3b"
    images = @($base64)
    prompt = "Describe this image briefly."
    stream = $false
} | ConvertTo-Json -Depth 10
$null = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -ContentType "application/json" -Body $body2
$swQwen.Stop()
Write-Host "qwen2.5vl:3b: $($swQwen.ElapsedMilliseconds)ms" -ForegroundColor Green

Write-Host ""
Write-Host "=== CLOUD GEMINI ===" -ForegroundColor Cyan
$swCloud = [Diagnostics.Stopwatch]::StartNew()
& "D:/Olympus/vision/analyze-image.ps1" $imgPath | Out-Null
$swCloud.Stop()
Write-Host "Cloud Gemini: $($swCloud.ElapsedMilliseconds)ms" -ForegroundColor Yellow

Write-Host ""
Write-Host "=== WINNER ===" -ForegroundColor Cyan
$times = @{
    "llava:13b" = $swLlava.ElapsedMilliseconds
    "qwen2.5vl:3b" = $swQwen.ElapsedMilliseconds
    "Cloud Gemini" = $swCloud.ElapsedMilliseconds
}
$winner = $times.GetEnumerator() | Sort-Object Value | Select-Object -First 1
Write-Host "$($winner.Key) wins at $($winner.Value)ms" -ForegroundColor Green
