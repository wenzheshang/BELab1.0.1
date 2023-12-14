echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 26704 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 60852) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 55524) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 60684)
del "f:\Thinking\program\BELab1.0.1_up\Workdata\Fluent_Python\2023-12-14_10-29\cleanup-fluent-wenzheshang-55524.bat"
