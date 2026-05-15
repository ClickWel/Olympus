$s = New-Object -ComObject WScript.Shell
$sc = $s.CreateShortcut('C:\Users\click\Desktop\Gemini Flash CC.lnk')
$sc.TargetPath = 'D:\Olympus\launchers\start-gemini-flash-free.bat'
$sc.Save()
