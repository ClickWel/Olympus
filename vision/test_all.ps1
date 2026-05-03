param($ImagePath)
$base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes((Resolve-Path $ImagePath)))
$models = @("qwen2.5vl:3b", "llava:13b")

foreach ($model in $models) {
    Write-Host "Testing model: $model"
    $body = @{
        model = $model
        prompt = "Describe this image"
        images = @($base64)
        stream = $false
    } | ConvertTo-Json -Depth 10
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -ContentType "application/json" -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
        Write-Host "Response: $($response.response)"
    } catch {
        Write-Host "Error with ${model}: $($_.Exception.Message)"
    }
}
