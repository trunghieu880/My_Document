#!/bin/bash

CANTATA_OUTPUT="./UT_008_RBAPLPLANT_WriteDataByIdentifier_BB80833"

func_name="RBAPLPLANT_WriteDataByIdentifier"

find ${CANTATA_OUTPUT} > ./_lst_find_

## CHECK FILE SOURCE ###
check_file_c=`grep -c "src_tst/${func_name}\.c$" ./_lst_find_`
check_file_doc=`grep -c "doc/${func_name}__CodeCoverage_or_Fail_Reason\.xls$" ./_lst_find_`

check_file_results_tpa=`grep -c "results/${func_name}.tpa" ./_lst_find_`
check_file_results_test_report_xml=`egrep -c "results/test_report.xml" ./_lst_find_`
check_file_results_test_report_html=`egrep -c "results/test_report.html" ./_lst_find_`
check_file_results_test_summary_html=`grep -c "results/test_summary.html" ./_lst_find_`

function check_content_tpa () {
  if [ $check_file_results_tpa -gt 0 ]
  then
    file_tpa=`grep "${func_name}.tpa" ./_lst_find_`
    const_UnitUnderTest="UnitUnderTest"
    const_NTUserID="NTUserID"
    const_FileName="FileName"
    const_Verdict="Verdict"
    const_MetricName="MetricName"
    const_Percentage="Percentage"

    temp="$const_UnitUnderTest"
    tpa_data_UnitUnderTest=`grep -o "${temp}>.*<" ${file_tpa} | sed -e "s/${temp}>//g" -e 's/<\///g' | sed 's/<//g' | sed 's/\s*\s//g'`

    temp="$const_NTUserID"
    tpa_data_NTUserID=`grep -o "${temp}>.*<" ${file_tpa} | sed -e "s/${temp}>//g" -e 's/<\///g' | sed 's/<//g' | sed 's/\s*\s//g'`

    temp="$const_FileName"
    tpa_data_FileName=`grep -o "${temp}>.*<" ${file_tpa} | sed -e "s/${temp}>//g" -e 's/<\///g' | sed 's/<//g' | sed 's/\s*\s//g'`

    temp="$const_Verdict"
    tpa_data_status=`grep -o "${temp}>.*<" ${file_tpa} | sed -e "s/${temp}>//g" -e 's/<\///g' | sed 's/<//g' | sed 's/\s*\s//g'`

    temp="$const_MetricName"
    tpa_data_score_C0=`grep -A 3 "${temp}>C0<" ${file_tpa} | grep -o "${const_Percentage}>.*<" | sed -e "s/${const_Percentage}>//g" | sed 's/<//g'`
    tpa_data_score_C1=`grep -A 3 "${temp}>C1<" ${file_tpa} | grep -o "${const_Percentage}>.*<" | sed -e "s/${const_Percentage}>//g" | sed 's/<//g'`
    tpa_data_score_MCDC=`grep -A 3 "${temp}>MC/DC<" ${file_tpa} | grep -o "${const_Percentage}>.*<" | sed -e "s/${const_Percentage}>//g" | sed 's/<//g'`
  fi
}

function check_content_test_report_xml () {
  if [ $check_file_results_test_report_xml -gt 0 ]
  then
    file_test_report_xml=`grep "results/test_report.xml" ./_lst_find_`
    const_FileName="srcFile"
    const_testScriptInfo="testScriptInfo"

    const_test_report_xml_coverageReport="coverageReport"
    const_test_report_xml_C0="statement"
    const_test_report_xml_C1="decision"
    const_test_report_xml_MCDC="booleanOperandEffectivenessUnique"

    temp="$const_test_report_xml_coverageInfo"
    test_report_xml_FileName=`grep -A 12 "<${temp}>" ${file_test_report_xml} | grep -o "${const_FileName} name=.* path" | sed 's/\s*\s/ /g' | awk '{print $2}' | sed 's/name=//g' | sed 's/"//g'`

    temp="$const_testScriptInfo"
    test_report_xml_status=`grep -A 2 "<${temp}>" ${file_test_report_xml} | grep -o "<summary status=.*>" | sed 's/<.*="//g' | sed 's/">.*//g'`

    temp="$const_test_report_xml_coverageInfo"
    test_report_xml_data_score_C0=`grep -A 12 "<${temp}>" ${file_test_report_xml} | grep -o "${const_test_report_xml_C0}>.*<" | sed -e "s/${const_test_report_xml_C0}>//g" | sed 's/<//g'`
    test_report_xml_data_score_C1=`grep -A 12 "<${temp}>" ${file_test_report_xml} | grep -o "${const_test_report_xml_C1}>.*<" | sed -e "s/${const_test_report_xml_C1}>//g" | sed 's/<//g'`
    test_report_xml_data_score_MCDC=`grep -A 12 "<${temp}>" ${file_test_report_xml} | grep -o "${const_test_report_xml_MCDC}>.*<" | sed -e "s/${const_test_report_xml_MCDC}>//g" | sed 's/<//g'`
  fi
}

function check_content_test_report_html () {
  if [ $check_file_results_test_report_html -gt 0 ]
  then
    file_test_report_html=`grep "results/test_report.html" ./_lst_find_`
    const_FileName="Source File"
    const_testScriptInfo="Test Script Info"

    const_test_report_html_coverageReport="Coverage Report"
    const_test_report_html_C0="Statement"
    const_test_report_html_C1="Decision"
    const_test_report_html_MCDC="Boolean Operand Effectiveness (Unique-Cause)"

    temp="$const_test_report_html_coverageReport"

    test_report_html_FileName=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_FileName} .*" | sed 's/\s*\s/ /g' | sed 's/<.*>//g' | awk '{print $NF}' | awk -F '\' '{print $NF}'`

    temp="$const_testScriptInfo"
    test_report_html_status=`grep -A 6 ">${temp}<" ${file_test_report_html} | grep -o ">Summary status<.*" | sed 's/Summary status.*<TD>//g' | sed 's/<.*>//g' | sed 's/>//g'`

    temp="$const_test_report_html_coverageReport"
    test_report_html_data_score_C0=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_test_report_html_C0}<.*>" | sed -e "s/${const_test_report_html_C0}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
    test_report_html_data_score_C1=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_test_report_html_C1}<.*>" | sed -e "s/${const_test_report_html_C1}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
    test_report_html_data_score_MCDC=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_test_report_html_MCDC}<.*>" | sed -e "s/${const_test_report_html_MCDC}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
  fi
}

function check_content_test_summary_html () {
  if [ $check_file_results_test_summary_html -gt 0 ]
  then
    file_test_summary_html=`grep "results/test_summary.html" ./_lst_find_`
    const_ProjectName="Project: "
    const_result="Overall Result: "

    const_test_summary_html_C0="Statement (S)"
    const_test_summary_html_C1="Decision (D)"
    const_test_summary_html_MCDC="MC/DC - unique cause (U)"

    temp="$const_ProjectName"

    test_summary_html_ProjectName=`grep -o ">${temp}<.*" ${file_test_summary_html} | sed "s/>${temp}//g" | sed 's/<\w>//g' | sed 's/<\W\w>//g'`

    set -x
    temp="$const_testScriptInfo"
    test_summary_html_status=`grep -A 6 ">${temp}<" ${file_test_summary_html} | grep -o ">Summary status<.*" | sed 's/Summary status.*<TD>//g' | sed 's/<.*>//g' | sed 's/>//g'`

    temp="$const_test_report_html_coverageReport"
    test_summary_html_data_score_C0=`grep -A 36 ">${temp}<" ${file_test_summary_html} | grep -o "${const_test_report_html_C0}<.*>" | sed -e "s/${const_test_report_html_C0}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
    test_summary_html_data_score_C1=`grep -A 36 ">${temp}<" ${file_test_summary_html} | grep -o "${const_test_report_html_C1}<.*>" | sed -e "s/${const_test_report_html_C1}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
    test_summary_html_data_score_MCDC=`grep -A 36 ">${temp}<" ${file_test_summary_html} | grep -o "${const_test_report_html_MCDC}<.*>" | sed -e "s/${const_test_report_html_MCDC}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
  fi
}

check_content_test_summary_html
