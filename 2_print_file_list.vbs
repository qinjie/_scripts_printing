Option Explicit

Function ReadLinesFromText(strTextFile)
	Dim objFSO, strData, strLines
	CONST ForReading = 1
	
	'Create a File System Object
	Set objFSO = CreateObject("Scripting.FileSystemObject")

	If objFSO.FileExists(strTextFile) Then 
		'Open the text file - strData now contains the whole file
		strData = objFSO.OpenTextFile(strTextFile, ForReading).ReadAll
	
		'Split the text file into lines
		strLines = Split(strData, vbCrLf)
		
		' Return
		ReadLinesFromText = strLines
	Else
		WScript.echo "File not exists"
		' Return
		ReadLinesFromText = Array
	End If
	
	Set objFSO = Nothing
End Function

' Main Program

if WScript.Arguments.Count <> 1 then
    WScript.Echo "Missing parameters"
    WScript.Quit 1
end If

Dim strFileList
strFileList = WScript.Arguments(0)

Dim objShell
Dim strLines, strLine
Dim intRunError

Const COL_COUNT = 1

Set objShell = CreateObject("WScript.Shell") 
' each line corresponding to one file
strLines = ReadLinesFromText(strFileList)

For Each strLine in strLines
	WScript.Echo strLine
	strLine = Trim(strLine)
	If strLine <> "" Then
		'Use notepad to print, add (1, true) to ensure it complete before proceed to next
		intRunError = objShell.Run("%COMSPEC% /c notepad /p " & strLine, 1, true)
		If intRunError <> 0 Then 
			WScript.Echo "Error printing " & strLine
		End If
		' Wait for 5 seconds bring print next student
		WScript.Sleep 1*1000
	End If
Next
WScript.Quit
