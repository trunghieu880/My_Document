import __init__
import logging
import os
from pathlib import Path
from unicodedata import normalize
import lxml.etree
import lxml.html
import parse, utils
import datetime
import const as CONST
import subprocess
import re
from docx.api import Document
import win32com.client
from win32com.client import Dispatch
import json

logger = logging.getLogger(__name__)

class Base(object):
    def __init__(self, path):
        self.path = Path(path)

class FileTPA(Base):
    # Class FileTPA
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.etree.parse(str(path))

    # Function get_tag: get the node of XML file with specific tag
    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

    # Function update_tag: update the node with the specific tag and value
    def update_tag(self, tag, value):
        self.get_tag(tag).text = value
        path = re.sub("file:/", "", self.doc.docinfo.URL)
        with open(path, 'wb') as f:
            self.doc.write(f)

    # Function update_tpa: update tpa file with the input data
    def update_tpa(self, data):
        lst_header = ["UnitUnderTest", "ExecutionDate", "NTUserID", "FileName", "Verdict"]

        for h in lst_header:
            self.update_tag(h, data[h])

        # collect Percentage Coverage
        lst_Percentage = [e for e in self.doc.iterfind('.//{0}'.format("Percentage"))]

        lst_Percentage[0].text = data['C0']
        lst_Percentage[1].text = data['C1']
        if utils.load(CONST.SETTING).get("sheetname") == "Merged_JOEM":
            lst_Percentage[2].text = data['MCDCU']

        path = re.sub("file:/", "", self.doc.docinfo.URL)
        with open(path, 'wb') as f:
            self.doc.write(f)

    # Function get_data: get the information in the Summary HTML file : "UnitUnderTest", "NTUserID", "FileName", "Verdict", "MetricName", "Percentage"
    def get_data(self):
        lst_header = ["UnitUnderTest", "NTUserID", "FileName", "Verdict", "MetricName", "Percentage"]
        ut = self.get_tag("UnitUnderTest").text
        user = self.get_tag("NTUserID").text
        func = self.get_tag("FileName").text
        result = self.get_tag("Verdict").text
        # collect title C0, C1, MC/DC
        lst_MetricName = [e.text for e in self.doc.iterfind('.//{0}'.format("MetricName"))]
        # collect Percentage Coverage
        lst_Percentage = [e.text for e in self.doc.iterfind('.//{0}'.format("Percentage"))]

        d = dict()
        lst_data = list()
        lst_data.append("NTUserID")
        lst_data.append(user)
        lst_data.append("FileName")
        lst_data.append(func)
        lst_data.append("TestResult")
        lst_data.append(result)

        for index, key in enumerate(lst_MetricName):
            lst_data.append(key)
            lst_data.append(lst_Percentage[index])

        # convert list to json
        d[ut] = {lst_data[i]: lst_data[i + 1] for i in range(0, len(lst_data), 2)}
        return d

class FileTestReportXML(Base):
    # Class FileTestReportXML
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.etree.parse(str(path))

    # Function get_tag: get the node of XML file with specific tag
    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

    # Function get_data: get the information in the Summary HTML file : Verdict, C0, C1, MCDC
    def get_data(self):
        lst_header = ["status", "statement", "decision", "booleanOperandEffectivenessMasking", "booleanOperandEffectivenessUnique", "testScriptName"]
        node_summary = self.get_tag("summary")
        status = {'Verdict': node_summary.attrib['status']}
        node_coverageInfo = self.get_tag("coverageInfo")[0]

        score = {'C0': item.text for item in node_coverageInfo if item.tag == "statement"}
        score = {**score, **{'C1': item.text for item in node_coverageInfo if item.tag == "decision"}}
        score = {**score, **{'MCDCM': item.text for item in node_coverageInfo if item.tag == "booleanOperandEffectivenessMasking"}}
        score = {**score, **{'MCDCU': item.text for item in node_coverageInfo if item.tag == "booleanOperandEffectivenessUnique"}}

        testscriptname = {'testScriptName': item.text for item in self.get_tag("info") if item.tag == "testScriptName"}

        data = dict()
        data = {**status, **score, **testscriptname}
        return data

class FileTestReportHTML(Base):
    # Class FileTestReportHTML
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.html.parse(str(path))

    # Function get_tag: get the node of html file with specific tag
    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

    # T.B.D
    def get_data(self):
        # file_test_report_html=`grep "results/test_report.html" ./_lst_find_`
        # const_FileName="Source File"
        # const_testScriptInfo="Test Script Info"

        # const_test_report_html_coverageReport="Coverage Report"
        # const_test_report_html_C0="Statement"
        # const_test_report_html_C1="Decision"
        # const_test_report_html_MCDC="Boolean Operand Effectiveness (Unique-Cause)"

        # temp="$const_test_report_html_coverageReport"

        # test_report_html_FileName=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_FileName} .*" | sed 's/\s*\s/ /g' | sed 's/<.*>//g' | awk '{print $NF}' | awk -F '\' '{print $NF}'`

        # temp="$const_testScriptInfo"
        # test_report_html_status=`grep -A 6 ">${temp}<" ${file_test_report_html} | grep -o ">Summary status<.*" | sed 's/Summary status.*<TD>//g' | sed 's/<.*>//g' | sed 's/>//g'`

        # temp="$const_test_report_html_coverageReport"
        # test_report_html_data_score_C0=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_test_report_html_C0}<.*>" | sed -e "s/${const_test_report_html_C0}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
        # test_report_html_data_score_C1=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_test_report_html_C1}<.*>" | sed -e "s/${const_test_report_html_C1}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
        # test_report_html_data_score_MCDC=`grep -A 36 ">${temp}<" ${file_test_report_html} | grep -o "${const_test_report_html_MCDC}<.*>" | sed -e "s/${const_test_report_html_MCDC}.*<TD>//g" | sed 's/<.*>//g' | sed 's/<//g' | sed 's/%//g'`
        pass

class FileTestSummaryHTML(Base):
    # Class FileTestSummaryHTML
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.html.parse(str(path))

    # Function get_tag: get the node of html file with specific tag
    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

    # Function get_data: get the information in the Summary HTML file : Verdict, C0, C1, MCDC
    def get_data(self):
        data = dict()
        try:
            for e in self.doc.iterfind('.//{0}'.format("div")):
                if e.text == None:
                    continue
                if "Project:" in e.text or "Overall Result:" in e.text:
                    for item in e:
                        if "Project:" in e.text:
                            data = {**data, **{'Project': item.text}}
                        elif "Overall Result:" in e.text:
                            data = {**data, **{'Verdict': item.text}}
                        else:
                            print("BUG FileTestSummaryHTML get_data")
        
            key = ""
            flag = False
            for e in self.doc.iterfind('.//{0}'.format("div")):
                if e.text == None:
                    continue
                if e.text == "Statement (S)" or e.text == "Decision (D)" or e.text == "MC/DC - masking (M)" or e.text == "MC/DC - unique cause (U)":
                    flag = True
                    if e.text == "Statement (S)":
                        key = "C0"
                    elif e.text == "Decision (D)":
                        key = 'C1'
                    elif e.text == "MC/DC - masking (M)":
                        key = 'MCDCM'
                    elif e.text == "MC/DC - unique cause (U)":
                        key = 'MCDCU'
                    else:
                        raise("BUG")
                    next
                else:
                    if "%" in e.text and flag == True:
                        flag = False
                        val = e.text.replace("%", "")
                        data = {**data, key : val}
                        key = ""
                        val = ""
                        next
                    else:
                        continue
        except Exception as e:
            data = {}
            raise(e)
        finally:
            return data

class FileCoverageReasonXLS(Base):
    def __init__(self, path):
        super().__init__(path)
        self.doc = str(path)

    # Function update_tpa: update tpa file with the input data
    def update(self, data):
        excel = win32com.client.Dispatch('Excel.Application')
        wb = excel.Workbooks.Open(self.doc)
        excel.Visible = False
        excel.DisplayAlerts = False
        wb.DoNotPromptForConvert = True
        wb.CheckCompatibility = False

        score_c0 = (value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA")
        score_c1 = (value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C1") != None) else "NA")
        score_mcdc = (value(int(float(value(data.get("MCDC"))) * 100)) if (value(data.get("MCDC")) != "-" and data.get("MCDC") != None) else "NA")

        data_tpa = {
            "UnitUnderTest": data.get("ItemName"),
            "NTUserID": str(convert_name(key=data.get("Tester"), opt="id")),
            "ExecutionDate" : datetime.datetime.now().strftime("%Y-%m-%d"),
            "C0": score_c0,
            "C1": score_c1,
            "MCDCU": score_mcdc
        }

        writeData = wb.Worksheets(1)
        # Write data here
        infor_CoverageReasonXLS = utils.load(CONST.SETTING).get("CoverageReasonXLS")

        writeData.Range(infor_CoverageReasonXLS.get("Tester")).Value = data_tpa.get("NTUserID")
        writeData.Range(infor_CoverageReasonXLS.get("Date")).Value = data_tpa.get("ExecutionDate")
        writeData.Range(infor_CoverageReasonXLS.get("Item_Name")).Value = data_tpa.get("UnitUnderTest")
        writeData.Range(infor_CoverageReasonXLS.get("C0")).Value = data_tpa.get("C0")
        writeData.Range(infor_CoverageReasonXLS.get("C1")).Value = data_tpa.get("C1")
        writeData.Range(infor_CoverageReasonXLS.get("MCDC")).Value = data_tpa.get("MCDCU")

        wb.Save()
        wb.Close()
        excel.Quit()
        excel = None

    # Function get_data: to get the array data with specfic key, value of the nested json
    def get_data(self):
        excel = win32com.client.Dispatch('Excel.Application')
        wb = excel.Workbooks.Open(self.doc)

        excel.Visible = False
        excel.DisplayAlerts = False
        wb.DoNotPromptForConvert = True
        wb.CheckCompatibility = False

        readData = wb.Worksheets(1)
        allData = readData.UsedRange

        infor_CoverageReasonXLS = utils.load(CONST.SETTING).get("CoverageReasonXLS")

        data = {
            "Tester": value(allData.Cells(1, 2).value),
            "Date": value(allData.Cells(2, 2).value),
            "Item_Name": value(allData.Cells(3, 2).value),
            "C0": value(int(float(allData.Cells(9, 2).value))),
            "C1": value(int(float(allData.Cells(10, 2).value))),
            "MCDC": value(int(float(allData.Cells(11, 2).value)))
        }

        wb.Save()
        wb.Close()
        excel.Quit()
        excel = None
        return data

class FileSummaryXLSX(Base):
    # Class FileSummaryXLSX
    def __init__(self, path):
        super().__init__(path)
        self.doc = str(path)

    # Function parse2json: convert XLSX to json data
    def parse2json(self, sheetname="", begin=47, end=47):
        return dict(parse.parse_summary_json(self.doc, sheetname=sheetname, begin=begin, end=end))

    # Function get_data: to get the array data with specfic key, value of the nested json
    def get_data(self, data, key, value):
        item = -1
        d = dict()
        for item in data.keys():
            if(data[item].get(key) == value):
                d[item] = data[item]

        return d

# Check the directory of function is exist or not
def check_exist(dir_input, function):
    return Path(dir_input).joinpath(function).exists()

# Convert Tester name to Real Name or USERID
def convert_name(key, opt="name"):
    logger.debug("Convert name")
    try:
        users = utils.load(CONST.SETTING).get("users")

        if opt == "name" or opt == "id":
            return str(users[key].get(opt))
        else:
            raise("Bug convert name")
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Check path : have src extension or not
def is_have_src(path):
    return ("\\src" in path or "\\SRC" in path)

# Trim Component Path to find the correct path
def trim_src(path):
    result = re.sub("^.*\\\\rb\\\\", "rb\\\\", path)
    result = re.sub("^.*\\\\rba\\\\", "rba\\\\", result)
    result = re.sub("\\\\src\\\\.*$", "", result)
    result = re.sub("\\\\SRC\\\\.*$", "", result)
    result = re.sub("\\\\src$", "", result)
    result = re.sub("\\\\SRC$", "", result)
    return result

def value(cell):
    if str(cell).isdigit():
        return str(cell)
    else:
        return str(cell)

# Check information between summary xlsx, and test_summay_html is same or not
def check_information(file_test_summary_html, data, function_with_prj_name="", file_test_report_xml="", file_tpa="", file_CoverageReasonXLS="", opt=""):
    try:
        data_test_summary = FileTestSummaryHTML(file_test_summary_html).get_data()
        
        logger.debug("Check information {}", data.get("ItemName").replace(".c", ""))
        count = 0
        flag = False

        temp = ""
        if (utils.load(CONST.SETTING).get("sheetname") == "Merged_JOEM"):
            temp = function_with_prj_name
        else:
            temp = data.get("ItemName").replace(".c", "")
        
        if data_test_summary.get("Project") == temp:
            flag = True
        else:
            flag = False
            logger.error("Different ItemName {} - {}".format(data_test_summary.get("Project"), temp))
            return False

        if data_test_summary.get("Verdict") == "Pass":
            flag = True
        else:
            flag = False
            logger.error("ItemName {} got Verdict: {} - {}".format(data_test_summary.get("Project"), data_test_summary.get("Verdict"), data.get("Status Result")))
            return False

        if ((data_test_summary.get("C0") == (value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"))
                and data_test_summary.get("C1") == (value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C1") != None) else "NA")
                and data_test_summary.get("MCDCU") == (value(int(float(value(data.get("MCDC"))) * 100)) if (value(data.get("MCDC")) != "-" and data.get("MCDC") != None) else "NA")):
            flag = True
        else:
            flag = False
            logger.error("ItemName Test Summary {} has different C0: {}/{}; C1: {}/{}; MCDC: {}/{}".format(data_test_summary.get("Project"), data_test_summary.get("C0"), (value(int(float(value(data.get("C0"))) * 100))),
                                                                        data_test_summary.get("C1"), (value(int(float(value(data.get("C1"))) * 100))),
                                                                        data_test_summary.get("MCDCU"), (value(int(float(value(data.get("MCDC"))) * 100))))
                        )
            return False

        if (utils.load(CONST.SETTING).get("sheetname") == "Merged_JOEM"):
            # Check information between FileTPA and Summary
            if (opt == "check_tpa_xls"):
                data_tpa = FileTPA(file_tpa).get_data()
                data_tpa = data_tpa[data.get("ItemName").replace(".c", "") + ".c"]
                if ((data_tpa.get("C0") == (value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"))
                        and data_tpa.get("C1") == (value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C1") != None) else "NA")
                        and data_tpa.get("MC/DC") == (value(int(float(value(data.get("MCDC"))) * 100)) if (value(data.get("MCDC")) != "-" and data.get("MCDC") != None) else "NA")):
                    flag = True
                else:
                    flag = False
                    logger.error("ItemName TPA {} has different C0: {}/{}; C1: {}/{}; MCDC: {}/{}".format(data_tpa.get("FileName").replace(".c", ""), data_test_summary.get("C0"), (value(int(float(value(data.get("C0"))) * 100))),
                                                                                data_tpa.get("C1"), (value(int(float(value(data.get("C1"))) * 100))),
                                                                                data_tpa.get("MC/DC"), (value(int(float(value(data.get("MCDC"))) * 100))))
                                )
                    return False
            
            # Check information between FileTestReportXML and Summary
            data_test_report_xml = FileTestReportXML(file_test_report_xml).get_data()

            if ((data_test_report_xml.get("C0") == (value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"))
                    and data_test_report_xml.get("C1") == (value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C1") != None) else "NA")
                    and data_test_report_xml.get("MCDCU") == (value(int(float(value(data.get("MCDC"))) * 100)) if (value(data.get("MCDC")) != "-" and data.get("MCDC") != None) else "NA")):
                flag = True
            else:
                flag = False
                logger.error("ItemName Test Report XML {} has different C0: {}/{}; C1: {}/{}; MCDC: {}/{}".format(data_test_report_xml.get("testScriptName"), data_test_report_xml.get("C0"), (value(int(float(value(data.get("C0"))) * 100))),
                                                                            data_test_report_xml.get("C1"), (value(int(float(value(data.get("C1"))) * 100))),
                                                                            data_test_report_xml.get("MCDCU"), (value(int(float(value(data.get("MCDC"))) * 100))))
                                                                            )
                return False

            if (opt == "check_tpa_xls"):
                # Check information between FileCoverageReasonXLS and Summary
                data_CoverageReasonXLS = FileCoverageReasonXLS(file_CoverageReasonXLS).get_data()
                if ((data_CoverageReasonXLS.get("C0") == (value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"))
                        and data_CoverageReasonXLS.get("C1") == (value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C1") != None) else "NA")
                        and data_CoverageReasonXLS.get("MCDC") == (value(int(float(value(data.get("MCDC"))) * 100)) if (value(data.get("MCDC")) != "-" and data.get("MCDC") != None) else "NA")):
                    flag = True
                else:
                    flag = False
                    print(value(int(float(data_CoverageReasonXLS.get("C1")))))
                    logger.error("ItemName FileCoverageReasonXLS {} has different C0: {}/{}; C1: {}/{}; MCDC: {}/{}".format(data_CoverageReasonXLS.get("Item_Name"), data_CoverageReasonXLS.get("C0"), (value(int(float(value(data.get("C0"))) * 100))),
                                                                                data_CoverageReasonXLS.get("C1"), (value(int(float(value(data.get("C1"))) * 100))),
                                                                                data_CoverageReasonXLS.get("MCDC"), (value(int(float(value(data.get("MCDC"))) * 100))))
                                                                                )
                    return False

        return flag
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Check Release for JOEM is correct ot not
def check_archives_joem(path_summary, dir_input, taskids, begin=47, end=47):
    logger.debug("Start checker: Archives")
    try:
        doc = FileSummaryXLSX(path_summary)
        data = doc.parse2json(begin=begin, end=end)

        file_log = open("log_delivery.txt", "w")

        print("Start checker: Archives")
        print("*****************************************************************")
        file_log.write("Start checker: Archives\n")
        file_log.write("*****************************************************************\n")

        for taskid in taskids["TaskGroup"]:
            temp_data_prj = doc.get_data(data=data, key="Project", value=taskids["Project"])
            data_taskid = doc.get_data(data=temp_data_prj, key="TaskGroup", value=taskid)
            bb_number = taskids["BB"]
            path_taskid = Path(dir_input).joinpath(str(taskid))
            if (path_taskid.exists()):
                count = 0
                for item in data_taskid.keys():
                    function = data_taskid[item].get("ItemName").replace(".c", "")
                    user_tester = data_taskid[item].get("Tester")
                    mt_number = data_taskid[item].get("MT_Number").replace("UT_", "").replace("MT_", "")

                    if "ASW" == data_taskid[item].get("Type"):
                        mt_number = "MT_" + mt_number
                        logging.warning("{},{},{},{}".format(taskid, function, user_tester, "NG_MT_Check_Later"))
                        file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG_MT_Check_Later"))
                        continue
                    elif "PSW" == data_taskid[item].get("Type"):
                        mt_number = "UT_" + mt_number
                    else:
                        mt_number = "NONE"
                        print("BUG mt_number")

                    folder_mt_function = "{}_{}_{}".format(mt_number, function, bb_number)

                    b_check_exist = check_exist(dir_input=path_taskid, function=folder_mt_function)
                    if (b_check_exist):
                        count += 1
                        
                        file_tpa = Path(path_taskid).joinpath(folder_mt_function, "Cantata", "results", "{}.tpa".format(function))
                        file_CoverageReasonXLS = Path(path_taskid).joinpath(folder_mt_function, "doc", "{}_{}".format(function, "CodeCoverage_or_Fail_Reason.xls"))
                        file_test_report_xml = Path(path_taskid).joinpath(folder_mt_function, "Cantata", "results", "test_report.xml")
                        file_test_summary = Path(path_taskid).joinpath(folder_mt_function, "Cantata", "results", "test_summary.html")

                        option_check = ""
                        if (len(str(function)) < 32):
                            option_check = "check_tpa_xls"
                        else:
                            option_check = ""

                        if check_information(file_test_summary_html=file_test_summary, data=data_taskid[item], function_with_prj_name=folder_mt_function, file_test_report_xml=file_test_report_xml, file_tpa=file_tpa, file_CoverageReasonXLS=file_CoverageReasonXLS, opt=option_check):
                            print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                            file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "OK"))
                        else:
                            logger.error("Different Information {},{},{},{}".format(taskid, function, user_tester, "NG_DiffInfor"))
                            file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG_DiffInfor"))

                    else:
                        logging.warning("{},{},{},{}".format(taskid, function, user_tester, "NG"))
                        file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG"))

                num_tpa = len(utils.scan_files(directory=path_taskid, ext=".tpa")[0])
                status = ["GOOD" if (num_tpa == len(data_taskid)) and (count == len(data_taskid)) else "BAD"][0]
                print("## Total {}: status {}: Found/Count/Total - {}/{}/{}".format(str(taskid), status, count, num_tpa, len(data_taskid)))
                print("-----------------------------------------------------------------\n")

                file_log.write("## Total {}: status {}: Found/Count/Total - {}/{}/{}\n".format(str(taskid), status, count, num_tpa, len(data_taskid)))
                file_log.write("-----------------------------------------------------------------\n")

            else:
                logger.warning("{} is not existed".format(path_taskid))
                file_log.write("{} is not existed\n".format(path_taskid))
                next

        print("FINISH")
        file_log.write("FINISH\n")
        file_log.close()

    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Check Release for JOEM is correct ot not
def make_archives_joem(path_summary, dir_input, dir_output, taskids, begin=47, end=47):
    logger.debug("Start checker: Make Archives JOEM")
    try:
        doc = FileSummaryXLSX(path_summary)
        data = doc.parse2json(begin=begin, end=end)

        file_log = open("log_delivery.txt", "w")

        print("Start checker: Make Archives JOEM")
        print("*****************************************************************")
        file_log.write("Start checker: Make Archives JOEM\n")
        file_log.write("*****************************************************************\n")

        for taskid in taskids["TaskGroup"]:
            temp_data_prj = doc.get_data(data=data, key="Project", value=taskids["Project"])
            data_taskid = doc.get_data(data=temp_data_prj, key="TaskGroup", value=taskid)
            bb_number = taskids["BB"]
            path_taskid = Path(dir_input).joinpath(str(taskid))
            if (path_taskid.exists()):
                count = 0
                for item in data_taskid.keys():
                    function = data_taskid[item].get("ItemName").replace(".c", "")
                    user_tester = data_taskid[item].get("Tester")
                    mt_number = data_taskid[item].get("MT_Number").replace("UT_", "").replace("MT_", "")

                    if "ASW" == data_taskid[item].get("Type"):
                        mt_number = "MT_" + mt_number
                        logging.warning("{},{},{},{}".format(taskid, function, user_tester, "NG_MT_Check_Later"))
                        file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG_MT_Check_Later"))
                        continue
                    elif "PSW" == data_taskid[item].get("Type"):
                        mt_number = "UT_" + mt_number
                    else:
                        mt_number = "NONE"
                        print("BUG mt_number")

                    folder_mt_function = "{}_{}_{}".format(mt_number, function, bb_number)

                    b_check_exist = check_exist(dir_input=path_taskid, function=folder_mt_function)
                    if (b_check_exist):
                        count += 1
                        
                        file_tpa = Path(path_taskid).joinpath(folder_mt_function, "Cantata", "results", "{}.tpa".format(function))
                        file_CoverageReasonXLS = Path(path_taskid).joinpath(folder_mt_function, "doc", "{}_{}".format(function, "CodeCoverage_or_Fail_Reason.xls"))
                        file_test_report_xml = Path(path_taskid).joinpath(folder_mt_function, "Cantata", "results", "test_report.xml")
                        file_test_summary = Path(path_taskid).joinpath(folder_mt_function, "Cantata", "results", "test_summary.html")

                        if check_information(file_test_summary_html=file_test_summary, data=data_taskid[item], function_with_prj_name=folder_mt_function, file_test_report_xml=file_test_report_xml, opt=""):
                            if (len(str(function)) < 32):
                                FileCoverageReasonXLS(file_CoverageReasonXLS).update(data_taskid[item])
                                utils.copy(src=Path(CONST.TEMPLATE).joinpath("template_joem.tpa"), dst=file_tpa)
                                update_tpa(file=file_tpa, data=data_taskid[item], file_test_summary_html=file_test_summary)

                                print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                                file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "OK"))
                            else:
                                logger.error("Long Name {},{},{},{}".format(taskid, function, user_tester, "NG_Long_Name"))
                                file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG_Long_Name"))
                        else:
                            logger.error("Different Information {},{},{},{}".format(taskid, function, user_tester, "NG_DiffInfor"))
                            file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG_DiffInfor"))

                    else:
                        logging.warning("{},{},{},{}".format(taskid, function, user_tester, "NG"))
                        file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG"))

                num_tpa = len(utils.scan_files(directory=path_taskid, ext=".tpa")[0])
                status = ["GOOD" if (num_tpa == len(data_taskid)) and (count == len(data_taskid)) else "BAD"][0]
                print("## Total {}: status {}: Found/Count/Total - {}/{}/{}".format(str(taskid), status, count, num_tpa, len(data_taskid)))
                print("-----------------------------------------------------------------\n")

                file_log.write("## Total {}: status {}: Found/Count/Total - {}/{}/{}\n".format(str(taskid), status, count, num_tpa, len(data_taskid)))
                file_log.write("-----------------------------------------------------------------\n")

            else:
                logger.warning("{} is not existed".format(path_taskid))
                file_log.write("{} is not existed\n".format(path_taskid))
                next

        print("FINISH")
        file_log.write("FINISH\n")
        file_log.close()

    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Check Release is correct or not
def check_releases(path_summary, dir_input, taskids, begin=47, end=47):
    logger.debug("Start checker: Release")

    try:
        doc = FileSummaryXLSX(path_summary)
        data = doc.parse2json(begin=begin, end=end)
        print("Start checker: Release")
        print("*****************************************************************")
        file_log = open("log_delivery.txt", "w")
        file_log.write("Start checker: Release\n")
        file_log.write("*****************************************************************\n")
        for taskid in taskids:
            print(taskid)
            data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
            path_taskid = Path(dir_input).joinpath(str(taskid), "RV")
            if (path_taskid.exists()):
                count = 0
                for item in data_taskid.keys():
                    function = data_taskid[item].get("ItemName").replace(".c", "")
                    user_tester = data_taskid[item].get("Tester")
                    b_check_exist = check_exist(dir_input=path_taskid, function=function)
                    if (b_check_exist):
                        count += 1
                        print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                        file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "OK"))

                    else:
                        logger.warning("{},{},{},{}".format(taskid, function, user_tester, "NG"))
                        file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG"))

                status = ["GOOD" if (len(os.listdir(path_taskid)) == len(data_taskid)) and (count == len(data_taskid)) else "BAD"][0]
                print("## Total {}: status {}: Found/Count/Total - {}/{}/{}".format(str(taskid), status, count, len(os.listdir(path_taskid)), len(data_taskid)))
                print("-----------------------------------------------------------------\n")

                file_log.write("## Total {}: status {}: Found/Count/Total - {}/{}/{}\n".format(str(taskid), status, count, len(os.listdir(path_taskid)), len(data_taskid)))
                file_log.write("-----------------------------------------------------------------\n")
            else:
                logger.error("{} is not existed".format(path_taskid))
                file_log.write("{} is not existed\n".format(path_taskid))
                next

        print("FINISH")
        file_log.write("FINISH\n")
        file_log.close()
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Check Archive is correct or not
def check_archives(path_summary, dir_input, taskids, begin=47, end=47):
    logger.debug("Start checker: Archives")
    try:
        doc = FileSummaryXLSX(path_summary)
        data = doc.parse2json(begin=begin, end=end)
        file_log = open("log_delivery.txt", "a")

        print("Start checker: Archives")
        print("*****************************************************************")
        file_log.write("Start checker: Archives\n")
        file_log.write("*****************************************************************\n")
        for taskid in taskids:
            data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
            path_taskid = Path(dir_input).joinpath(str(taskid), "AR")
            if (path_taskid.exists()):
                count = 0
                for item in data_taskid.keys():
                    function = data_taskid[item].get("ItemName").replace(".c", "")
                    user_tester = data_taskid[item].get("Tester")

                    path_with_component = Path(path_taskid).joinpath(str(trim_src(data_taskid[item].get("ComponentName"))), "Unit_tst", str(data_taskid[item].get("TaskID")))

                    b_check_exist = check_exist(dir_input=path_with_component, function=function)
                    if (b_check_exist):
                        count += 1
                        f_test_summary = Path(path_taskid).joinpath(path_with_component, function, "Test_Result", "test_summary.html")

                        if check_information(file_test_summary_html=f_test_summary, data=data_taskid[item]):
                            print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                            file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "OK"))
                        else:
                            logger.error("Different Information {},{},{},{}".format(taskid, function, user_tester, "NG_DiffInfor"))
                            file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG_DiffInfor"))

                    else:
                        logging.warning("{},{},{},{}".format(taskid, function, user_tester, "NG"))
                        file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG"))

                num_tpa = len(utils.scan_files(directory=path_taskid, ext=".tpa")[0])
                status = ["GOOD" if (num_tpa == len(data_taskid)) and (count == len(data_taskid)) else "BAD"][0]
                print("## Total {}: status {}: Found/Count/Total - {}/{}/{}".format(str(taskid), status, count, num_tpa, len(data_taskid)))
                print("-----------------------------------------------------------------\n")

                file_log.write("## Total {}: status {}: Found/Count/Total - {}/{}/{}\n".format(str(taskid), status, count, num_tpa, len(data_taskid)))
                file_log.write("-----------------------------------------------------------------\n")

            else:
                logger.warning("{} is not existed".format(path_taskid))
                file_log.write("{} is not existed\n".format(path_taskid))
                next

        print("FINISH")
        file_log.write("FINISH\n")
        file_log.close()

    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Update WalkThrough
def update_walkthrough(file, data, file_test_summary_html):
    logger.debug("Update Walkthrough {}", file)
    try:
        data_test_summary = FileTestSummaryHTML(file_test_summary_html).get_data()
        temp = str(trim_src(data.get("ComponentName"))) + "\\Unit_tst\\" + str(data.get("TaskID"))

        data_baseline = data.get("Baseline")
        if data_baseline == "None" or data_baseline == "":
            data_baseline = ""

        dict_walkthrough = {
            'date': datetime.datetime.now().strftime("%m/%d/%Y"),
            'project': data.get("ItemName"),
            'review initiator': convert_name(key=data.get("Tester"), opt="name"),
            'effort': str(0.5),
            'baseline': data_baseline,
            'review partner' : "Pham Thi Cam Vien (RBVH/EPS45)", #data.get("Owner Contact"),
            'path_testscript': temp + "\\Test_Spec",
            'path_test_summary': temp + "\\Test_Result",
            'ScoreC0C1': " Test summary\n\tC0: " + data_test_summary.get("C0") + "%\tC1: " + data_test_summary.get("C1") + "%",
        }

        document = Document(file)
        table_infor = document.tables[1]
        table_infor.cell(0,1).text = dict_walkthrough['date']
        table_infor.cell(0,3).text = dict_walkthrough['project']
        table_infor.cell(0,5).text = dict_walkthrough['review initiator']
        table_infor.cell(1,1).text = str(dict_walkthrough['effort'])
        table_infor.cell(1,3).text = dict_walkthrough['baseline']
        table_infor.cell(1,5).text = dict_walkthrough['review partner']
        table_attach = document.tables[2]
        table_attach.cell(1, 2).text = dict_walkthrough['path_testscript']
        table_attach.cell(3, 2).text = dict_walkthrough['path_test_summary']
        table_attach.cell(3, 1).text = dict_walkthrough['ScoreC0C1']
        document.save(file)
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Update File TPA
def update_tpa(file, data, file_test_summary_html):
    logger.debug("Update tpa {}", file)

    try:
        data_test_summary = FileTestSummaryHTML(file_test_summary_html).get_data()
        data_tpa = {
            "UnitUnderTest": data.get("ItemName").replace(".c", "") + ".c",
            "NTUserID": str(convert_name(key=data.get("Tester"), opt="id")),
            "ExecutionDate" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "FileName": data.get("ItemName"),
            "Verdict": data_test_summary.get('Verdict').replace("Pass", "Passed").replace("Fail", "Failed"),
            "C0": data_test_summary.get('C0'),
            "C1": data_test_summary.get('C1'),
            "MCDCU": data_test_summary.get('MCDCU'),
        }

        FileTPA(file).update_tpa(data_tpa)
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Encrypt file with 7z
def sevenzip(filename, zipname):
    zip_exe_path = utils.load(CONST.SETTING, "Tool_7z")
    with open(os.devnull, 'w') as null:
        subprocess.call([zip_exe_path, 'a', '-tzip', zipname, filename], stdout=null, stderr=null)

# Create Archive Walkthrough
def make_archieves(path_summary, dir_input, dir_output, taskids, begin=47, end=47):
    logger.debug("Create Archive Walkthrough")
    try:

        doc = FileSummaryXLSX(path_summary)
        data = doc.parse2json(begin=begin, end=end)

        print("Start checker: Make Archives")
        print("*****************************************************************")

        for taskid in taskids:
            data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
            path_taskid = Path(dir_input).joinpath(str(taskid), "RV")
            if (path_taskid.exists()):
                count = 0
                for item in data_taskid.keys():
                    function = data_taskid[item].get("ItemName").replace(".c", "")
                    user_tester = data_taskid[item].get("Tester")

                    # if function == "RBAPLCUST_RDBI_IOCtrlState" and taskid == 1416606:
                        # print("HERE")
                        # continue
                    b_check_exist = check_exist(dir_input=path_taskid, function=function)
                    if (b_check_exist):
                        count += 1

                        temp = str(data_taskid[item].get("C0"))
                        if (temp != "-" or temp != ""):
                            temp_component = str(data_taskid[item].get("ComponentName"))
                            if is_have_src(temp_component):
                                final_dst = Path(dir_output).joinpath(str(taskid), "AR", trim_src(temp_component), "Unit_tst", str(taskid), function)
                                dir_Configuration = Path(final_dst).joinpath("Configuration")
                                dir_Test_Spec = Path(final_dst).joinpath("Test_Spec")
                                dir_Test_Result = Path(final_dst).joinpath("Test_Result")

                                f_walkthrough = Path(dir_Test_Result).joinpath("Walkthrough_Protocol_" + function + ".docx")
                                f_tpa = Path(dir_Test_Result).joinpath(function + ".tpa")
                                f_test_summary = Path(path_taskid).joinpath(function, "Cantata", "results", "test_summary.html")

                                if check_information(file_test_summary_html=f_test_summary, data=data_taskid[item]):
                                    Path(dir_Configuration).parent.mkdir(parents=True, exist_ok=True)
                                    Path(dir_Configuration).mkdir(exist_ok=True)
                                    Path(dir_Test_Spec).mkdir(exist_ok=True)
                                    Path(dir_Test_Result).mkdir(exist_ok=True)

                                    utils.copy(src=Path(CONST.TEMPLATE).joinpath("WT_template.docx"), dst=f_walkthrough)
                                    utils.copy(src=Path(CONST.TEMPLATE).joinpath("template.tpa"), dst=f_tpa)
                                    utils.copy(src=f_test_summary, dst=dir_Test_Result)

                                    update_walkthrough(file=f_walkthrough, data=data_taskid[item], file_test_summary_html=f_test_summary)
                                    update_tpa(file=f_tpa, data=data_taskid[item], file_test_summary_html=f_test_summary)

                                    sevenzip(filename=Path(path_taskid).joinpath(function).as_posix(), zipname=Path(dir_Configuration).joinpath(str(function) + ".zip").as_posix())

                                    for f in utils.scan_files(directory=Path(path_taskid).joinpath(function, "Cantata", "tests"), ext=".c")[0]:
                                        sevenzip(filename=f.as_posix(), zipname=Path(dir_Test_Spec).joinpath(os.path.basename(f).replace(".c", ".zip")).as_posix())

                                    print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                                else:
                                    logger.error("Different information {},{},{},{}".format(taskid, function, user_tester, "NG"))
                                    next

                            else:
                                logger.error("Miss src in componentname {},{},{},{}".format(taskid, function, user_tester, "NG"))
                    else:
                        logger.warning("{},{},{},{}".format(taskid, function, user_tester, "NG"))
            else:
                next
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

def create_summary_json_file(file_summary, sheetname="", begin=47, end=47):
    # Generate json file
    if sheetname == "":
        sheetname = utils.load(CONST.SETTING).get("sheetname")

    file_log = Path(__file__).parent.joinpath("log_json", "{}_{}_{}.json".format("log_summary", sheetname, datetime.datetime.now().strftime("%Y_%m_%dT%H_%MZ"), ".json"))
    with open(file_log, errors='ignore', mode='w') as fp:
        json.dump(FileSummaryXLSX(file_summary).parse2json(sheetname=sheetname, begin=begin, end=end), fp, indent=4, sort_keys=True)

def collect_information_deliverables(file_summary, sheetname="", begin=47, end=47):
    if sheetname == "":
        sheetname = utils.load(CONST.SETTING).get("sheetname")

    data = FileSummaryXLSX(file_summary).parse2json(sheetname=sheetname, begin=begin, end=end)

    item = -1
    l_prj = list()
    for item in data.keys():
        if data[item].get("Project") is not None:
            l_prj.append(data[item].get("Project"))
    
    l_prj = list(set(l_prj))
    l_prj.sort()

    item = -1
    d = dict()

    for prj in l_prj:
        total_assign_asw = 0.0
        total_assign_psw = 0.0
        total_deliver_asw = 0.0
        total_deliver_psw = 0.0
        total_remain_asw = 0.0
        total_remain_psw = 0.0
        percentage_asw = 0.0
        percentage_psw = 0.0
        max_date_asw = ""
        max_date_psw = ""
        l_date_start_asw = list()
        l_date_end_asw = list()
        l_date_release_asw = list()
        l_date_start_psw = list()
        l_date_end_psw = list()
        l_date_release_psw = list()

        total_defect_asw = 0.0
        total_defect_psw = 0.0

        for item in data.keys():
            if(data[item].get("Project") == prj):
                if data[item].get("ELOC Recheck With Tool") is not None:
                    if "ASW" == data[item].get("Type"):
                        total_assign_asw += float(data[item].get("ELOC Recheck With Tool"))
                    elif "PSW" == data[item].get("Type"):
                        total_assign_psw += float(data[item].get("ELOC Recheck With Tool"))
                    else:
                        raise("BUG")
                else:
                    continue

                if data[item].get("LOC Complete") is not None:
                    # print("{},{},{},{}".format(item, prj, data[item].get("ItemName"),data[item].get("LOC Complete")))
                    if "ASW" == data[item].get("Type"):
                        total_deliver_asw += float(data[item].get("LOC Complete"))
                    elif "PSW" == data[item].get("Type"):
                        total_deliver_psw += float(data[item].get("LOC Complete"))
                    else:
                        raise("BUG")

                if data[item].get("Planned Start") is not None:
                    if "ASW" == data[item].get("Type"):
                        l_date_start_asw.append(data[item].get("Planned Start"))
                    elif "PSW" == data[item].get("Type"):
                        l_date_start_psw.append(data[item].get("Planned Start"))
                    else:
                        raise("BUG")

                if data[item].get("Planned End") is not None:
                    if "ASW" == data[item].get("Type"):
                        l_date_end_asw.append(data[item].get("Planned End"))
                    elif "PSW" == data[item].get("Type"):
                        l_date_end_psw.append(data[item].get("Planned End"))
                    else:
                        raise("BUG")

                if data[item].get("Release Date") is not None:
                    if "ASW" == data[item].get("Type"):
                        l_date_release_asw.append(data[item].get("Release Date"))
                    elif "PSW" == data[item].get("Type"):
                        l_date_release_psw.append(data[item].get("Release Date"))
                    else:
                        raise("BUG")

                if data[item].get("OPL/Defect") is not None:
                    if "ASW" == data[item].get("Type"):
                        if "Defect" == data[item].get("OPL/Defect"):
                            total_defect_asw += 1
                    elif "PSW" == data[item].get("Type"):
                        if "Defect" == data[item].get("OPL/Defect"):
                            total_defect_psw += 1
                    else:
                        raise("BUG")
                else:
                    continue


        date_start_asw = ""
        date_end_asw = ""
        date_release_asw = ""

        date_start_psw = ""
        date_end_psw = ""
        date_release_psw = ""

        if len(l_date_start_asw) == 0:
            date_start_asw = "NA"
        else:
            date_start_asw = min(l_date_start_asw)

        if len(l_date_end_asw) == 0:
            date_end_asw = "NA"
        else:
            date_end_asw = max(l_date_end_asw)

        if len(l_date_release_asw) == 0:
            date_release_asw = "NA"
        else:
            date_release_asw = max(l_date_release_asw)

        if len(l_date_start_psw) == 0:
            date_start_psw = "NA"
        else:
            date_start_psw = min(l_date_start_psw)

        if len(l_date_end_psw) == 0:
            date_end_psw = "NA"
        else:
            date_end_psw = max(l_date_end_psw)

        if len(l_date_release_psw) == 0:
            date_release_psw = "NA"
        else:
            date_release_psw = max(l_date_release_psw)

        total_remain_asw = total_assign_asw - total_deliver_asw
        total_remain_psw = total_assign_psw - total_deliver_psw

        if (total_assign_asw > 0):
            percentage_asw = round(total_deliver_asw/total_assign_asw * 100,2)
        elif (total_assign_asw == 0):
            percentage_asw = "NA"
        else:
            percentage_asw = "NG"

        if (total_assign_psw > 0):
            percentage_psw = round(total_deliver_psw/total_assign_psw * 100,2)
        elif (total_assign_psw == 0):
            percentage_psw = "NA"
        else:
            percentage_psw = "NG"

        template_json = {
            "Project": prj,
            "Type": "ASW",
            "Assigned task (ELOC)": total_assign_asw,
            "Assigned date": date_start_asw,
            "Target date": date_end_asw,
            "Delivered task (ELOC)": total_deliver_asw,
            "Delivered date": date_release_asw,
            "Remain (ELOC)": total_remain_asw, 
            "% Completion": percentage_asw
        }

        if total_assign_asw > 0:
            print("{},{},{},{},{},{},{},{},{},{}".format(prj, "ASW", total_assign_asw, date_start_asw, date_end_asw, total_deliver_asw, date_release_asw, total_remain_asw, percentage_asw, total_defect_asw))
        if total_assign_psw > 0:
            print("{},{},{},{},{},{},{},{},{},{}".format(prj, "PSW", total_assign_psw, date_start_psw, date_end_psw, total_deliver_psw, date_release_psw, total_remain_psw, percentage_psw, total_defect_psw))


    return l_prj

def make_folder_release(path_summary, l_packages, dir_output, begin=59, end=59):
    logger.debug("make_folder_release")
    try:
        doc = FileSummaryXLSX(path_summary)
        data = doc.parse2json(begin=begin, end=end)

        for package in l_packages:
            data_package = doc.get_data(data=data, key="Package", value=package)
            path_package = Path(dir_output).joinpath(str(package))
            for item in data_package.keys():
                Path(path_package).mkdir(exist_ok=True)

                taskid = data_package[item].get("TaskID")
                if taskid is not "None":
                    date_end = data_package[item].get("Planned End") if data_package[item].get("Planned End") != "None" else None
                    if date_end is not None:
                        date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S").strftime("%d-%b-%Y")
                        dir_taskid = Path(path_package).joinpath(str(date_end), str(taskid))
                        dir_taskid_RV = Path(dir_taskid).joinpath(str("RV"))
                        dir_taskid_AR = Path(dir_taskid).joinpath(str("AR"))
                        Path(dir_taskid).parent.mkdir(parents=True, exist_ok=True)
                        Path(dir_taskid).mkdir(exist_ok=True)
                        Path(dir_taskid_RV).mkdir(exist_ok=True)
                        Path(dir_taskid_AR).mkdir(exist_ok=True)

                    else:
                        log.warning("Not filling Planned Start/Planned End")
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done")

# Main
def main():
    try:
        file_summary = utils.load(CONST.SETTING).get("file_summary")
        dir_input = utils.load(CONST.SETTING).get("dir_input_coem")
        dir_output = utils.load(CONST.SETTING).get("dir_output")
        sheetname = utils.load(CONST.SETTING).get("sheetname")

        l_taskids = utils.load(CONST.SETTING).get("l_taskids_coem")
        if sheetname == "Merged_JOEM":
            l_taskids = utils.load(CONST.SETTING).get("l_taskids_joem_20200525")

        """Make folder release"""
        # make_folder_release(path_summary=file_summary, l_packages=[20200601], dir_output=dir_output, begin=59, end=1000)

        """Create json file of summary to backup"""
        # create_summary_json_file(file_summary=file_summary, sheetname="Merged_COEM", begin=47, end=1000)
        # create_summary_json_file(file_summary=file_summary, sheetname="Merged_JOEM", begin=47, end=1000)

        """Collect information for deliverables"""
        # collect_information_deliverables(file_summary=file_summary, sheetname="Merged_COEM", begin=59, end=1000)

        for opt in utils.load(CONST.SETTING).get("mode_coem"):
            if opt == "check_releases":
                check_releases(path_summary=file_summary, dir_input=dir_input, taskids=l_taskids, begin=59, end=1000)
            elif opt == "check_archives":
                if sheetname == "Merged_JOEM":
                    check_archives_joem(path_summary=file_summary, dir_input=dir_input, taskids=l_taskids, begin=59, end=400)
                else:
                    check_archives(path_summary=file_summary, dir_input=dir_input, taskids=l_taskids, begin=59, end=1000)
            elif opt == "make_archives":
                if sheetname == "Merged_JOEM":
                    make_archives_joem(path_summary=file_summary, dir_input=dir_input, dir_output=dir_output, taskids=l_taskids, begin=59, end=400)
                else:
                    make_archieves(path_summary=file_summary, dir_input=dir_input, dir_output=dir_output, taskids=l_taskids, begin=59, end=400)
            else:
                raise("I dont know your mode")
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Done)")

if __name__ == "__main__":
    main()
