echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 27029 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 62724) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 56032) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 62236)
del "f:\Thinking\program\BELab1.0.1_up\Workdata\Fluent_Python\2023-12-14_10-41\cleanup-fluent-wenzheshang-56032.bat"
