Add-Type -AssemblyName System.Windows.Forms
if ([System.Windows.Forms.Clipboard]::ContainsImage()) {
    $img = [System.Windows.Forms.Clipboard]::GetImage()
    $img.Save('D:\Olympus\clipboard_screenshot.png', [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output 'Saved clipboard to D:\Olympus\clipboard_screenshot.png'
} else {
    Write-Output 'No image on clipboard'
}
