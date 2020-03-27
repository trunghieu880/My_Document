@echo off

set MODULE_NAME=%1
set PRODUCT=%2
set AUTOSAR_VERSION=%3
set CONFIG=%4


REM set LIST_OF_FILE=Dio.c.html

set QAC_REPORT_LOC="U:\internal\X1X\%PRODUCT%\modules\%MODULE_NAME%\test_static\qac\%AUTOSAR_VERSION%\%CONFIG%"

:: check qac path exist
if Not Exist %QAC_REPORT_LOC% (
	echo Path is not exist: %QAC_REPORT_LOC%
	echo.
	goto HELP
)

for  /R %QAC_REPORT_LOC% %%f in (*.c.html) do (
	echo %%~nxf
	REM echo %%f
	call T3_67.pl -msn=%MODULE_NAME% -family=%PRODUCT% -f=%%~nxf -iheader -checkdup > %AUTOSAR_VERSION%_%CONFIG%_%%~nxf.log
)
echo.
goto End


:HELP
@echo off.
REM Cls
echo Usage:
echo qac.bat Msn Family Autosar Config
echo.
echo Msn               - Module Short Name to be generated e.g. Port, Can, Adc,...
echo.
echo Family            - Chip Family Name e.g. F1X, P1X-C, P1X-E, P1X,...
echo.
echo Autosar           - Autosar version e.g. 4.0.3 or 4.2.2
echo.           
echo Config            - Config run for QAC e.g. cfg01, cfg02,...           
echo.           
goto :END
echo.

:END
echo Done!!!
echo.