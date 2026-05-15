Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d D:\Olympus\gemini-for-claude-code && pythonw.exe server.py", 0, False
Set WshShell = Nothing
