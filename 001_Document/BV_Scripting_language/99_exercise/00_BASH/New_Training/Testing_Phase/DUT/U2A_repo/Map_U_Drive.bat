::##############################################################################
:: Purpose: To map U drive
:: Usage  : Map_U_Drive.bat <directory to map>
::##############################################################################
@ECHO OFF
SET CURRENT_DIR=%CD%
SETLOCAL
IF EXIST U: SUBST U: /D

IF EXIST %CURRENT_DIR% (
   SUBST U: %CURRENT_DIR%
   ECHO Current virtual drive map is ....
   SUBST
) ELSE ECHO %CURRENT_DIR% is not existed.

ENDLOCAL
@ECHO ON
