#!/bin/bash

SUMMARY_FILE="/c/Users/hieu.nguyen-trung/Desktop/Summary_performance_BV.xlsx"
SHEET_NAME="COEM_Package_20200302"

XLSX2CSV="/c/Users/hieu.nguyen-trung/AppData/Local/Programs/Python/Python37/python.exe /c/Users/hieu.nguyen-trung/AppData/Local/Programs/Python/Python37/Lib/site-packages/xlsx2csv.py"

my_dir_script="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd ${my_dir_script}

${XLSX2CSV} -n ${SHEET_NAME} ${SUMMARY_FILE} | sed -n "/^,No,Package,.*$/,/^,Table KPI ASW,/p" | grep -v '^,Table KPI ASW' > .TEMP_SUMMARY

COL_NO=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "No.") {print i; break}; i++}}'`
COL_PACKAGE=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "File") {print i; break}; i++}}'`
COL_TYPE=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Group") {print i; break}; i++}}'`
COL_PROJECT=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Function") {print i; break}; i++}}'`
COL_COMPONENTNAME=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "LOC") {print i; break}; i++}}'`
COL_TASKID=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "PIC") {print i; break}; i++}}'`
COL_ITEMNAME=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Peer Review") {print i; break}; i++}}'`
COL_DATABASE=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Vol") {print i; break}; i++}}'`
COL_ITEMREVISION=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Result") {print i; break}; i++}}'`
COL_TESTER=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Result") {print i; break}; i++}}'`
COL_LOC=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Result") {print i; break}; i++}}'`
COL_STATUS=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Result") {print i; break}; i++}}'`
COL_C0=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "C0") {print i; break}; i++}}'`
COL_C1=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "C1") {print i; break}; i++}}'`
COL_MCDC=`grep "^No." .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "MC/DC") {print i; break}; i++}}'`
