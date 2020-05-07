import logging
import os
from pathlib import Path
from unicodedata import normalize

import lxml.etree
import lxml.html

import parse, utils
import datetime

import subprocess
import re

from docx.api import Document

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
        # lst_Percentage[2].text = data['MCDCU']

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
        lst_header = ["status", "statement", "decision", "booleanOperanndEffectivenessMasking", "booleanOperanndEffectivenessUnique", "testScriptName"]
        node_summary = self.get_tag("summary")
        status = {'Verdict': node_summary.attrib['status']}
        node_coverageInfo = self.get_tag("coverageInfo")[0]

        score = {'C0': item.text for item in node_coverageInfo if item.tag == "statement"}
        score = {**score, **{'C1': item.text for item in node_coverageInfo if item.tag == "decision"}}
        score = {**score, **{'MCDCM': item.text for item in node_coverageInfo if item.tag == "booleanOperanndEffectivenessMasking"}}
        score = {**score, **{'MCDCU': item.text for item in node_coverageInfo if item.tag == "booleanOperanndEffectivenessUnique"}}

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
        for e in self.doc.iterfind('.//{0}'.format("div")):
            if "Project:" in e.text or "Overall Result:" in e.text:
                for item in e:
                    if "Project:" in e.text:
                        data = {**data, **{'Project': item.text}}
                    elif "Overall Result:" in e.text:
                        data = {**data, **{'Verdict': item.text}}
                    else:
                        print("BUG FileTestSummaryHTML get_data")
        try:
            key = ""
            flag = False
            for e in self.doc.iterfind('.//{0}'.format("div")):
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

class FileXLS(Base):
    # T.B.D
    pass

class FileSummaryXLSX(Base):
    # Class FileSummaryXLSX
    def __init__(self, path):
        super().__init__(path)
        self.doc = str(path)

    # Function parse2json: convert XLSX to json data
    def parse2json(self, begin=47, end=47):
        return dict(parse.parse_summary_json(self.doc, begin=begin, end=end))

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

# Check Release is correct or not
def check_releases(path_summary, dir_input, taskids, begin=47, end=47):
    doc = FileSummaryXLSX(path_summary)
    data = doc.parse2json(begin=begin, end=end)

    file_log = open("log_delivery.txt", "w")
    print("Start checker: Release")
    print("*****************************************************************")
    file_log.write("Start checker: Release\n")
    file_log.write("*****************************************************************\n")
    for taskid in taskids:
        data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
        path_taskid = Path(dir_input).joinpath(str(taskid) + str("\\RV"))
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
                    print("{},{},{},{}".format(taskid, function, user_tester, "NG"))
                    file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG"))

            status = ["GOOD" if (len(os.listdir(dir_input + "\\" + str(taskid) + "\\RV")) == len(data_taskid)) and (count == len(data_taskid)) else "BAD"][0]
            print("## Total {}: status {}: Found/Count/Total - {}/{}/{}".format(str(taskid), status, count, len(os.listdir(path_taskid)), len(data_taskid)))
            print("-----------------------------------------------------------------\n")

            file_log.write("## Total {}: status {}: Found/Count/Total - {}/{}/{}\n".format(str(taskid), status, count, len(os.listdir(path_taskid)), len(data_taskid)))
            file_log.write("-----------------------------------------------------------------\n")



        else:
            print("{} is not existed".format(path_taskid))
            file_log.write("{} is not existed\n".format(path_taskid))
            next

    print("FINISH")
    file_log.write("FINISH\n")
    file_log.close()

# Check Archive is correct or not
def check_archives(path_summary, dir_input, taskids, begin=47, end=47):
    doc = FileSummaryXLSX(path_summary)
    data = doc.parse2json(begin=begin, end=end)

    file_log = open("log_delivery.txt", "w")
    print("Start checker: Archives")
    print("*****************************************************************")
    file_log.write("Start checker: Archives\n")
    file_log.write("*****************************************************************\n")
    for taskid in taskids:
        data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
        path_taskid = Path(dir_input).joinpath(str(taskid) + str("\\AR"))
        if (path_taskid.exists()):
            count = 0
            for item in data_taskid.keys():
                function = data_taskid[item].get("ItemName").replace(".c", "")
                user_tester = data_taskid[item].get("Tester")
                b_check_exist = check_exist(dir_input=path_taskid.as_posix().replace("/", "\\") + "\\" + str(trim_src(data_taskid[item].get("ComponentName"))) + "\\Unit_tst\\" + str(data_taskid[item].get("TaskID")), function=function)
                if (b_check_exist):
                    count += 1
                    print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                    file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "OK"))

                else:
                    print("{},{},{},{}".format(taskid, function, user_tester, "NG"))
                    file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG"))

            num_tpa = len(utils.scan_files(directory=path_taskid, ext=".tpa")[0])
            status = ["GOOD" if (num_tpa == len(data_taskid)) and (count == len(data_taskid)) else "BAD"][0]
            print("## Total {}: status {}: Found/Count/Total - {}/{}/{}".format(str(taskid), status, count, num_tpa, len(data_taskid)))
            print("-----------------------------------------------------------------\n")

            file_log.write("## Total {}: status {}: Found/Count/Total - {}/{}/{}\n".format(str(taskid), status, count, num_tpa, len(data_taskid)))
            file_log.write("-----------------------------------------------------------------\n")

        else:
            print("{} is not existed".format(path_taskid))
            file_log.write("{} is not existed\n".format(path_taskid))
            next

    print("FINISH")
    file_log.write("FINISH\n")
    file_log.close()

# Convert Tester name to Real Name or USERID
def convert_name(key, opt="name"):
    data = {
        'hieu.nguyen-trung': {'name': "Nguyen Trung Hieu", 'id': "nhi5hc"},
        'hau.nguyen-tai': {'name': "Nguyen Tai Hau", 'id': "nah4hc"},
        'bang.nguyen-duy': {'name': "Nguyen Duy Bang", 'id': "nbg7hc"},
        'dac.luu-cong': {'name': "Luu Cong Dac", 'id': "lud5hc"},
        'duong.nguyen': {'name': "Nguyen Tuan Duong", 'id': "ndy4hc"},
        'loc.do-phu': {'name': "Do Phu Loc", 'id': "dol7hc"},
        'thanh.nguyen-kimhieu': {'name': "Nguyen Kim Thanh", 'id': "nut4hc"},
        'chung.ly': {'name': "Ly Chung", 'id': "lyc1hc"},
        'huy.do-anh': {'name': "Do Anh Huy", 'id': "duh7hc"},
        'phuong.nguyen-thanh': {'name': "Nguyen Thanh Phuong", 'id': "gup7hc"}
    }
    if opt == "name":
        return str("EXTERNAL " + data[key].get(opt) + " (Ban Vien, RBVH/EPS45)")
    elif opt == "id":
        return str(data[key].get(opt))
    else:
        print("BUG convert_name")

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
def check_information(file_test_summary_html, data):
    data_test_summary = FileTestSummaryHTML(file_test_summary_html).get_data()

    count = 0
    flag = False

    if data_test_summary.get("Project") == data.get("ItemName").replace(".c", ""):
        flag = True
    else:
        flag = False
        return False

    if data_test_summary.get("C0") == (value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"):
        flag = True
    else:
        flag = False
        return False

    if data_test_summary.get("C1") == (value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C1") != None) else "NA"):
        flag = True
    else:
        flag = False
        return False

    if data_test_summary.get("MCDCU") == (value(int(float(value(data.get("MCDC"))) * 100)) if (value(data.get("MCDC")) != "-" and data.get("MCDC") != None) else "NA"):
        flag = True
    else:
        flag = False
        return False

    return True

# Update WalkThrough
def update_walkthrough(file, data, file_test_summary_html):
    data_test_summary = FileTestSummaryHTML(file_test_summary_html).get_data()
    temp = str(trim_src(data.get("ComponentName"))) + "\\Unit_tst\\" + str(data.get("TaskID"))
    # score_c0 = [value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"][0]
    # score_c1 = [value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C0") != None) else "NA"][0]
    
    data_baseline = data.get("Baseline")
    if data_baseline == "None" or data_baseline = "":
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

# Update File TPA
def update_tpa(file, data, file_test_summary_html):
    data_test_summary = FileTestSummaryHTML(file_test_summary_html).get_data()
    data_tpa = {
        "UnitUnderTest": data.get("ItemName"),
        "NTUserID": str(convert_name(key=data.get("Tester"), opt="id")),
        "ExecutionDate" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "FileName": data.get("ItemName"),
        "Verdict": data_test_summary.get('Verdict').replace("Pass", "Passed").replace("Fail", "Failed"),
        "C0": data_test_summary.get('C0'),
        "C1": data_test_summary.get('C1'),
        "MCDCU": data_test_summary.get('MCDCU'),
    }

    FileTPA(file).update_tpa(data_tpa)

# Encrypt file with 7z
def sevenzip(filename, zipname):
    zip_exe_path = "C:\\Program Files\\7-Zip\\7z.exe"
    with open(os.devnull, 'w') as null:
        subprocess.call([zip_exe_path, 'a', '-tzip', zipname, filename], stdout=null, stderr=null)

# Create Archive Walkthrough
def make_archieves(path_summary, dir_input, dir_output, taskids, begin=47, end=47):
    doc = FileSummaryXLSX(path_summary)
    data = doc.parse2json(begin=begin, end=end)

    for taskid in taskids:
        data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
        path_taskid = Path(dir_input).joinpath(str(taskid) + str("\\RV"))
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
                            final_dst = dir_output + "\\" + str(taskid) + "\\AR\\" + trim_src(temp_component) + "\\Unit_tst\\" + str(taskid) + "\\" + function
                            dir_Configuration = final_dst + "\\Configuration"
                            dir_Test_Spec = final_dst + "\\Test_Spec"
                            dir_Test_Result = final_dst + "\\Test_Result"

                            f_walkthrough = dir_Test_Result + "\\Walkthrough_Protocol_" + function + ".docx"
                            f_tpa = dir_Test_Result + "\\" + function + ".tpa"
                            f_test_summary = path_taskid.as_posix().replace("/", "\\") + "\\" + function + "\\Cantata\\results\\test_summary.html"

                            if check_information(file_test_summary_html=f_test_summary, data=data_taskid[item]):
                                Path(dir_Configuration).parent.mkdir(parents=True, exist_ok=True)
                                Path(dir_Configuration).mkdir(exist_ok=True)
                                Path(dir_Test_Spec).mkdir(exist_ok=True)
                                Path(dir_Test_Result).mkdir(exist_ok=True)

                                utils.copy(src=".\\template\\WT_template.docx", dst=f_walkthrough)
                                utils.copy(src=".\\template\\template.tpa", dst=f_tpa)
                                utils.copy(src=f_test_summary, dst=dir_Test_Result + "\\")

                                update_walkthrough(file=f_walkthrough, data=data_taskid[item], file_test_summary_html=f_test_summary)
                                update_tpa(file=f_tpa, data=data_taskid[item], file_test_summary_html=f_test_summary)

                                sevenzip(filename=path_taskid.as_posix().replace("/", "\\") + "\\" + function, zipname=dir_Configuration + "\\" + str(function) + ".zip")

                                for f in utils.scan_files(directory=path_taskid.as_posix().replace("/", "\\") + "\\" + function + "\\Cantata\\tests", ext=".c")[0]:
                                    sevenzip(filename=f.as_posix().replace("/", "\\"), zipname=dir_Test_Spec + "\\" + os.path.basename(f).replace(".c", ".zip"))
                                print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                            else:
                                print("Bug: different information {},{},{},{}".format(taskid, function, user_tester, "NG"))
                                next

                        else:
                            print("Bug: miss src in componentname {},{},{},{}".format(taskid, function, user_tester, "NG"))
                else:
                    print("{},{},{},{}".format(taskid, function, user_tester, "NG"))

            status = (len(os.listdir(dir_input + "\\" + str(taskid))) == len(data_taskid)) and (count == len(data_taskid))
        else:
            next

# Main
def main():
    # file_summary = "C:\\Users\\hieu.nguyen-trung\\Desktop\\Summary_JOEM.xlsm"
    # dir_input="C:\\Users\\hieu.nguyen-trung\\Desktop\\check"
    # dir_output = "C:\\Users\\hieu.nguyen-trung\\Desktop\\OUTPUT"
    file_summary = r"//hc-ut40346c/NHI5HC/hieunguyen/0000_Project/001_Prj/02_JOEM/Summary_JOEM_COEM_20200501.xlsm".replace("/", "\\")
    release_date="06-May-2020"
    # release_date="28-Apr-2020"
    dir_input = r"//hc-ut40346c/NHI5HC/hieunguyen/0000_Project/001_Prj/02_JOEM/01_Output_Package/20200429/COEM".replace("\\", "\\\\") + "\\" + release_date
    # dir_input="\\\\10.184.143.103\\d\\vivi\\BV\\Release\\JOEM\\28-Apr-2020"
    # dir_input="C:\\Users\\nhi5hc\\Desktop\\bbbb\\24-Apr-2020"
    dir_output = r"C:/Users/nhi5hc/Desktop/OUTPUT".replace("/", "\\") + "\\" + release_date

    # l_taskids = [1416009]
    # l_taskids = [1411690,1411700,1417738,1423830,1423829] # Group 24-Apr-2020
    # l_taskids = [1424417] # Group 28-Apr-2020
    # l_taskids = [1426302,1425475,1420442,1404793] # Group 29-Apr-2020
    # l_taskids = [1416607,1416606,1417780] # Group 30-Apr-2020
    # l_taskids = [1435905,1439160,1439436,1417033] # Group 5-May-2020
    l_taskids = [1439430,1416489,1442021] # Group 6-May-2020

    check_releases(path_summary=file_summary, dir_input=dir_input, taskids=l_taskids, begin=47, end=400)
    check_archives(path_summary=file_summary, dir_input=dir_input, taskids=l_taskids, begin=47, end=400)
    #make_archieves(path_summary=file_summary, dir_input=dir_input, dir_output=dir_output, taskids=l_taskids, begin=47, end=400)
    print("Complete")


if __name__ == "__main__":
    main()
