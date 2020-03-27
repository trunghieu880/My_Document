@echo off

title Renesas Console
SET PATH=%PATH%;U:\external\X1X\F1x\common_family\make\ghs
SET PATH=%PATH%;U:\internal\X1X\F1x\common_family\make\ghs
SET PATH=%PATH%;U:\internal\X1X\common_platform\generic\generator
SET PATH=%PATH%;U:\internal\X1X\common_platform\generic\qac

echo.Build^> Starting Shell...
echo.USAGE:
echo.SampleApp - to compile sample application
echo.TstApp    - to build test application
echo.Utility   - to perform stack and RAM/ROM measurement
echo.BuildTool - to create generator tool executable
echo.Qac       - to run QAC analysis
echo.
echo.NOTE: commands are case insensitive
echo.
SET prompt=$G

CALL C:\Windows\System32\cmd.exe
PAUSE