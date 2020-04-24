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
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.etree.parse(str(path))

    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

    def update_tag(self, tag, value):
        self.get_tag(tag).text = value
        path = re.sub("file:/", "", self.doc.docinfo.URL)
        with open(path, 'wb') as f:
            self.doc.write(f)

    def update_tpa(self, data):
        lst_header = ["UnitUnderTest", "ExecutionDate", "NTUserID", "FileName", "Verdict"]

        for h in lst_header:
            self.update_tag(h, data[h])

        # collect Percentage Coverage
        lst_Percentage = [e for e in self.doc.iterfind('.//{0}'.format("Percentage"))]

        lst_Percentage[0].text = data['C0']
        lst_Percentage[1].text = data['C1']
#        lst_Percentage[2].text = data['MCDCM']

        path = re.sub("file:/", "", self.doc.docinfo.URL)
        with open(path, 'wb') as f:
            self.doc.write(f)

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
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.etree.parse(str(path))

    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

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

        print('')

class FileTestReportHTML(Base):
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.html.parse(str(path))
    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

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
    def __init__(self, path):
        super().__init__(path)
        self.doc = lxml.html.parse(str(path))
    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

    def get_data(self):
        node = [e for e in self.doc.iterfind('.//{0}'.format("td"))]
        status = ""
        for e in self.doc.iterfind('.//{0}'.format("td")):
            for item in e:
                if item.text == "PASSED" or item.text == "FAILED":
                    if item.text == "PASSED":
                        status = "PASSED"
                        break
                    elif item.text == "FALSED":
                        status = "FAILED"
                        break
                    else:
                        raise("BUG")

        data = dict()
        data = {'Verdict': status}
        try:
            for e in self.doc.iterfind('.//{0}'.format("td")):
                for item in e:
                    if item.text == "Statement (S)" or item.text == "Decision (D)" or item.text == "MC/DC - masking (M)" or item.text == "MC/DC - unique cause (U)":
                        if item.text == "Statement (S)":
                            key = "C0"
                        elif item.text == "Decision (D)":
                            key = 'C1'
                        elif item.text == "MC/DC - masking (M)":
                            key = 'MCDCM'
                        elif item.text == "MC/DC - unique cause (U)":
                            key = 'MCDCU'
                        else:
                            raise("BUG")
                        next
                    else:
                        if "%" in item.text:
                            val = item.text
                            data = {**data, key : val}
                            next
                        else:
                            continue

        except Exception as e:
            raise(e)

class FileXLS(Base):
    pass

class FileSummaryXLSX(Base):
    def __init__(self, path):
        super().__init__(path)
        self.doc = str(path)

    def parse2json(self, begin=47, end=47):
        return dict(parse.parse_summary_json(self.doc, begin=begin, end=end))

    def get_tag(self, tag, index=0):
        '''Get normalized text of tag base on index of tag'''
        node = [e for e in self.doc.iterfind('.//{0}'.format(tag))][index]
        return node

    def get_data(self, data, key, value):
        # data = self.parse2json()
        item = -1
        d = dict()
        for item in data.keys():
            if(data[item].get(key) == value):
                d[item] = data[item]

        return d

def check_exist(dir_input, function):
    return Path(dir_input).joinpath(function).exists()

def check_releases(path_summary, dir_input, taskids, begin=47, end=47):
    # path_summary = "D:\\Material\\GIT\\My_Document\\999_NW\\Test_Folder\\Local_Summary.xlsm"
    #path_summary = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\Summary_JOEM.xlsm"
    doc = FileSummaryXLSX(path_summary)

    data = doc.parse2json(begin=begin, end=end)
    # taskids = [1415974, 1416009, 1416093, 1416090, 1417373, 1417493, 1416608, 1390624, 1420664, 1414211, 1414361, 1416225, 1417633, 1413225] # FULL deadline 17APR
    # dir_input = "\\\\10.184.143.103\\d\\vivi\\BV\\Release\\20200417"

    file_log = open("log_delivery.txt", "w")
    print("Start checker: Release")
    print("*****************************************************************")
    file_log.write("Start checker: Release\n")
    file_log.write("*****************************************************************\n")
    for taskid in taskids:
        data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
        path_taskid = Path(dir_input).joinpath(str(taskid) + str("\\RV"))
        #path_taskid = Path(dir_input).joinpath(str("RV") + str(taskid))
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

def check_archives(path_summary, dir_input, taskids, begin=47, end=47):
    # path_summary = "D:\\Material\\GIT\\My_Document\\999_NW\\Test_Folder\\Local_Summary.xlsm"
    #path_summary = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\Summary_JOEM.xlsm"
    doc = FileSummaryXLSX(path_summary)

    data = doc.parse2json(begin=begin, end=end)
    # taskids = [1415974, 1416009, 1416093, 1416090, 1417373, 1417493, 1416608, 1390624, 1420664, 1414211, 1414361, 1416225, 1417633, 1413225] # FULL deadline 17APR
    # dir_input = "\\\\10.184.143.103\\d\\vivi\\BV\\Release\\20200417"

    file_log = open("log_delivery.txt", "w")
    print("Start checker: Archives")
    print("*****************************************************************")
    file_log.write("Start checker: Archives\n")
    file_log.write("*****************************************************************\n")
    for taskid in taskids:
        data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
        path_taskid = Path(dir_input).joinpath(str(taskid) + str("\\AR"))
        #path_taskid = Path(dir_input).joinpath(str("RV") + str(taskid))
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

def convert_name(name, opt="n"):
    if opt == "n":
        if name == "hieu.nguyen-trung":
            name = "Nguyen Trung Hieu"
        elif name == "hau.nguyen-tai":
            name = "Nguyen Tai Hau"
        elif name == "bang.nguyen-duy":
            name = "Nguyen Duy Bang"
        elif name == "dac.luu-cong":
            name = "Luu Cong Dac"
        elif name == "duong.nguyen":
            name = "Nguyen Tuan Duong"
        elif name == "loc.do-phu":
            name = "Do Phu Loc"
        elif name == "thanh.nguyen-kim":
            name = "Nguyen Kim Thanh"
        elif name == "chung.ly":
            name = "Ly Chung"
        elif name == "huy.do-anh":
            name = "Do Anh Huy"
        elif name == "phuong.nguyen-thanh":
            name = "Nguyen Thanh Phuong"
        else:
            name = "Unknown"

        return str("EXTERNAL " + name + " (Ban Vien, RBVH/EPS45)")
    else:
        if name == "hieu.nguyen-trung":
            name = "nhi5hc"
        elif name == "hau.nguyen-tai":
            name = "nah4hc"
        elif name == "bang.nguyen-duy":
            name = "nbg7hc"
        elif name == "dac.luu-cong":
            name = "lud5hc"
        elif name == "duong.nguyen":
            name = "ndy4hc"
        elif name == "loc.do-phu":
            name = "dol7hc"
        elif name == "thanh.nguyen-kim":
            name = "nut4hc"
        elif name == "chung.ly":
            name = "lyc1hc"
        elif name == "huy.do-anh":
            name = "duh7hc"
        elif name == "phuong.nguyen-thanh":
            name = "gup7hc"
        else:
            name = "Unknown"
        return str(name)

def is_have_src(path):
    if "\\src" in path or "\\SRC" in path:
        return True
    else:
        return False

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

def update_walkthrough(file, data):
    temp = str(trim_src(data.get("ComponentName"))) + "\\Unit_tst\\" + str(data.get("TaskID"))
    score_c0 = [value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"][0]
    score_c1 = [value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C0") != None) else "NA"][0]
    dict_walkthrough = {
        'date': datetime.datetime.now().strftime("%m/%d/%Y"),
        'project': data.get("ItemName"),
        'review initiator': convert_name(name=data.get("Tester")),
        'effort': str(0.5),
        'baseline': data.get("Baseline"),
#        'review partner' : data.get("Owner Contact"),
        'review partner' : "Pham Thi Cam Vien (RBVH/EPS45)",
        'path_testscript': temp + "\\Test_Spec",
        'path_test_summary': temp + "\\Test_Result",
        'ScoreC0C1': "Test summary\n       C0: " + str(score_c0) + "%        C1: " + str(score_c1) + "%",
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

def update_tpa(file, data):
    data_tpa = {
        "UnitUnderTest": data.get("ItemName"),
        "NTUserID": str(convert_name(data.get("Tester"), opt="u")),
        "ExecutionDate" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "FileName": data.get("ItemName"),
        "Verdict": data.get("Status Result"),
        "C0": [value(int(float(value(data.get("C0"))) * 100)) if (value(data.get("C0")) != "-" and data.get("C0") != None) else "NA"][0],
        "C1": [value(int(float(value(data.get("C1"))) * 100)) if (value(data.get("C1")) != "-" and data.get("C1") != None) else "NA"][0],
        "MCDCM": [value(int(float(value(data.get("MCDC"))) * 100)) if (value(data.get("MCDC")) != "-" and data.get("MCDC") != None) else "NA"][0]
    }

    FileTPA(file).update_tpa(data_tpa)

def sevenzip(filename, zipname):
    zip_exe_path = "C:\\Program Files\\7-Zip\\7z.exe"
    subprocess.call([zip_exe_path, 'a', '-tzip', zipname, filename])

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
                            dir_Test_Summary = final_dst + "\\Test_Summary"

                            Path(dir_Configuration).parent.mkdir(parents=True, exist_ok=True)
                            Path(dir_Configuration).mkdir(exist_ok=True)
                            Path(dir_Test_Spec).mkdir(exist_ok=True)
                            Path(dir_Test_Summary).mkdir(exist_ok=True)

                            f_walkthrough = dir_Test_Summary + "\\WalkThrough_Protocol_" + function + ".docx"
                            f_tpa = dir_Test_Summary + "\\" + function + ".tpa"
                            utils.copy(src=".\\template\\WT_template.docx", dst=f_walkthrough)
                            utils.copy(src=".\\template\\template.tpa", dst=f_tpa)
                            update_walkthrough(file=f_walkthrough, data=data_taskid[item])
                            update_tpa(file=f_tpa, data=data_taskid[item])

                            sevenzip(filename=path_taskid.as_posix().replace("/", "\\") + "\\" + function, zipname=dir_Configuration + "\\" + str(function) + ".zip")
                            utils.copy(src=path_taskid.as_posix().replace("/", "\\") + "\\" + function + "\\Cantata\\results\\test_summary.html", dst=dir_Test_Summary + "\\")

                            for f in utils.scan_files(directory=path_taskid.as_posix().replace("/", "\\") + "\\" + function + "\\Cantata\\tests", ext=".c")[0]:
                                sevenzip(filename=f.as_posix().replace("/", "\\"), zipname=dir_Test_Spec + "\\" + os.path.basename(f).replace(".c", ".zip"))

                        else:
                            print("Bug: " + temp_component)

                        print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                else:
                    print("{},{},{},{}".format(taskid, function, user_tester, "NG"))

            status = (len(os.listdir(dir_input + "\\" + str(taskid))) == len(data_taskid)) and (count == len(data_taskid))
        else:
            next

def main():
    # file_summary = "D:\\Material\\GIT\\My_Document\\999_NW\\Test_Folder\\Sample\\Summary_JOEM.xlsm"
    #file_summary = "C:\\Users\\hieu.nguyen-trung\\Desktop\\Summary_JOEM.xlsm"
    #dir_input="C:\\Users\\hieu.nguyen-trung\\Desktop\\check"
    #dir_output = "C:\\Users\\hieu.nguyen-trung\\Desktop\\OUTPUT"
    file_summary = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\Summary_JOEM.xlsm"
#HieuNguyen     dir_input="\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\01_Output_Package\\20200416_1_20200417_20200420\\24-Apr-2020"
    dir_input="C:\\Users\\nhi5hc\\Desktop\\bbbb\\24-Apr-2020"
    dir_output = "C:\\Users\\nhi5hc\\Desktop\\OUTPUT"

    # l_taskids = [1411690,1411700,1417738,1423830,1423829] # Group 24-Apr-2020
    l_taskids = [1411690,1411700,1417738,1423830,1423829] # Group 28-Apr-2020
    
    check_releases(path_summary=file_summary, dir_input=dir_input, taskids=l_taskids, begin=47, end=400)
    check_archives(path_summary=file_summary, dir_input=dir_input, taskids=l_taskids, begin=47, end=400)
    # make_archieves(path_summary=file_summary, dir_input=dir_input, dir_output=dir_output, taskids=l_taskids, begin=47, end=400)
    print("Complete")


if __name__ == "__main__":
    main()
