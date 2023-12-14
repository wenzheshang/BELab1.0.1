echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 26883 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 61896) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 61348) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 59140)
del "f:\Thinking\program\BELab1.0.1_up\Workdata\Fluent_Python\2023-12-14_10-35\cleanup-fluent-wenzheshang-61348.bat"
