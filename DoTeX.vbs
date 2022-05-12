Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c DoTeX.bat"
oShell.Run strArgs, 0, false