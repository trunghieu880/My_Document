ECHO OFF
REM ############################################################################
REM ## AUTHOR: VIETNGUYEN
REM ## DATE  : DEC 20 2016
REM ## DECS  : THIS TOOL INTERGRATION WITH AMDC TOOL FOR CHECKING THE 
REM ##         CORRECTNESS OF PDFs BY GENERATE REPORT IN EXCEL FORMAT
REM ############################################################################

SET ArgCount=0
SET ARGV=1
FOR %%x IN (%*) DO SET /A ArgCount+=1
REM ## SETTINGS INVIRONMENT
IF %ArgCount% LSS %ARGV% (
    ECHO CONFIG BY CONFIG FILE
    CALL config.bat
    
) ELSE (
    ECHO CONFIG BY PASSING ARGUMENTS
    SET AMDC_PATH=%1
    SET PDFs_LOCATION_PATH=%2
)

SET PATH=%AMDC_PATH%;%PATH%;
REM ############################################################################

REM ## CLEAR OLD FILEs
IF EXIST ".\Report" (

    DEL /Q /F .\Report\*

) ELSE (
    MKDIR ".\Report"
)

REM ## PROCESSING
ECHO ANALYSING...
Amdc.exe -s "%PDFs_LOCATION_PATH%" > AMDC.log
perl .\scripts\AMDC_log_analysis.plx
ECHO DONE!
MOVE /Y ".\AMDC_Report.xlsx" ".\Report\AMDC_Report.xlsx"
MOVE /Y ".\*.log" ".\Report"
ECHO OPEN REPORT!
start excel ".\Report\AMDC_Report.xlsx"
ECHO FINISHED!
REM ## END #####################################################################
PAUSE
