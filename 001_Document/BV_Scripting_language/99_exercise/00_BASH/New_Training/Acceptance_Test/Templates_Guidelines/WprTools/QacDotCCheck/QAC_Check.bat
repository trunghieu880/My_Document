@echo off
setlocal EnableDelayedExpansion

SET MSN=%1
SET AR=%2
IF "%2%"=="4.0.3" SET AR_TOOL=4_0_3
IF "%2%"=="4.2.2" SET AR_TOOL=4_2_2
SET DEVICE=F1x
SET ROOT_FOLDER=U:\internal\X1X
SET TOOl_FOLDER=%cd%

IF /i "%1"=="" (
GOTO :Help
)
IF "%2" NEQ "4.2.2" IF "%2" NEQ "4.0.3" (
GOTO :Help
)

CALL :CONV_VAR_to_MAJ MSN
IF EXIST output\%DEVICE%\%MSN%\%AR_TOOL%\ (
RD /S /Q output\%DEVICE%\%MSN%\%AR_TOOL%\
)
MKDIR output\%DEVICE%\%MSN%\%AR_TOOL%\merge\output\error
IF NOT EXIST "U:\temp\output_merge\temp" MKDIR "U:\temp\output_merge\temp"
CD /D "%ROOT_FOLDER%\%DEVICE%\modules\%MSN%\test_static\qac\%AR%"
FOR /D %%D in (*) DO (
SET CFG=!CFG! %%~nxD
XCOPY "%ROOT_FOLDER%\%DEVICE%\modules\%MSN%\test_static\qac\%AR%\%%~nxD\output\*.c" "%TOOl_FOLDER%\output\%DEVICE%\%MSN%\%AR_TOOL%\%%~nxD\output\" /S /Y
IF /i "%MSN%"=="cortst" (
DEL "%TOOl_FOLDER%\output\%DEVICE%\%MSN%\%AR_TOOL%\%%~nxD\output\sw_cst.c"
)
)
CD /D %TOOl_FOLDER%
CALL .\scripts\Merge_Tool.exe %MSN%\%AR_TOOL% %CFG% F1x C:\Workspace\Jenkins\Tool\QAC
CALL .\scripts\CWM_Tool.exe %MSN%\%AR_TOOL% %DEVICE% C:\Workspace\Jenkins\Tool\QAC
CALL .\scripts\MWC_Tool.exe %MSN%\%AR_TOOL% .\output\Messages.txt %DEVICE% C:\Workspace\Jenkins\Tool\QAC

goto :End

:CONV_VAR_to_MAJ
FOR %%z IN (a b c d e f g h i j k l m n o p q r s t u v w x y z) DO CALL set %~1=%%%~1:%%z=%%z%%
GOTO :eof

:Help
echo.
echo ===========================================================================
echo                        HELP TO BUILD QAC tool
echo ===========================================================================
echo Usage:
echo.
echo QAC_Check.bat MODULE_NAME AUTOSAR_VERSION
echo.
echo MODULE_NAME      -   Module Short Name to be generated e.g. Port, CanV2,
echo                      Adc, ...
echo.
echo AUTOSAR_VERSION  -   AutoSAR version to be compiled which is available
echo                      4.0.3 or 4.2.2
echo ===========================================================================
goto :END

:End

ENDLOCAL

@echo on