param(
    [Parameter(Mandatory=$true)][string]$ImagePath,
    [string]$Engine = "local"
)

if (-not (Test-Path $ImagePath)) { Write-Error "Image not found: $ImagePath"; exit 1 }

switch ($Engine) {
    "gemini" {
        $apiKey = $env:GOOGLE_GENERATIVE_AI_API_KEY
        if (-not $apiKey) { 
            $apiKey = "***REMOVED***"
        }
        $mimeType = switch -Regex ((Get-Item $ImagePath).Extension) {
            '\.png$' { "image/png" }
            '\.jpe?g$' { "image/jpeg" }
            '\.gif$' { "image/gif" }
            '\.webp$' { "image/webp" }
            default { "image/png" }
        }
        $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes((Resolve-Path $ImagePath)))
        
        $prompt = "Describe this image in detail. Focus on any text, data, UI elements, or information that would be useful for an AI assistant to understand the content."
        
        $jsonPayload = @"
{
  "contents": {
    "parts": [
      {"inlineData": {"mimeType": "$mimeType", "data": "$base64"}},
      {"text": "$prompt"}
    ]
  }
}
"@
        
        $tempFile = [System.IO.Path]::GetTempFileName() + ".json"
        $jsonPayload | Out-File -FilePath $tempFile -Encoding utf8
        
        $url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$apiKey"
        $response = Invoke-RestMethod -Uri $url -Method Post -ContentType "application/json" -Body (Get-Content $tempFile -Raw)
        Remove-Item $tempFile -Force
        
        Write-Output $response.candidates[0].content.parts[0].text
    }
    "local" {
        $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes((Resolve-Path $ImagePath)))
        $body = @{
            model = "qwen2.5vl:3b"
            stream = $false
            images = @($base64)
            prompt = "Describe this image in detail. Focus on any text, data, UI elements, or information that would be useful for an AI assistant to understand the content."
        } | ConvertTo-Json -Depth 10
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -ContentType "application/json" -Body $body
        Write-Output $response.response
    }
}
