:: 1. Copy this .bat file to SampleApp.bat location
:: 2. Set Device list
:: 3. Set Output storing log results
:: 4. Run SampleAppRun.bat <msn> <arVer>

@echo off
setlocal EnableDelayedExpansion

IF /i "%1"=="" (
GOTO :Help
)
IF "%2" NEQ "4.2.2" IF "%2" NEQ "4.0.3" (
GOTO :Help
)

SET msn=%1
SET arVer=%2
SET devList=701623 701622
SET ouput=U:\internal\X1X\F1x\modules\%msn%\test_acceptance\F1K_F1KM\Ver4.04.00.B_Ver42.04.00.B\Results\SampleApp

FOR %%d in (%devList%) do (
Call SampleApp.bat %msn% %arVer% %%d >Log_%%d_%arVer%.txt 2>&1
xcopy Log_%%d_%arVer%.txt %ouput% /e /D /Y
)

:Help
echo.
echo ===========================================================================
echo                        HELP TO RUN SAMPLE APPLICATION FULL DEVICES
echo ===========================================================================
echo Usage:
echo.
echo. Set Device list in SampleAppRun.bat
echo.
echo. Set Output path in SampleAppRun.bat
echo.
echo  Run SampleAppRun.bat msn arVer
echo.
echo  msn    -   Module Short Name to be generated e.g. Port, CanV2,
echo.
echo  arVer  -   AutoSAR version to be compiled which is available
echo             4.0.3 or 4.2.2
echo.
echo ===========================================================================

ENDLOCAL
