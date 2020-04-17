import logging
import os
from pathlib import Path
from unicodedata import normalize

import lxml.etree
import lxml.html

import parse, utils

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

def check_exist(directory, function):
    return Path(directory).joinpath(function).exists()

def main():
    # path_summary = "D:\\Material\\GIT\\My_Document\\999_NW\\Test_Folder\\Local_Summary.xlsm"
    path_summary = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\Summary_JOEM.xlsm"
    doc = FileSummaryXLSX(path_summary)

    data = doc.parse2json(begin=47, end=227)
    taskids = [1415974, 1416009, 1416093, 1416090, 1417373, 1417493, 1416608, 1390624, 1420664, 1414211, 1414361, 1416225, 1417633, 1413225] # FULL deadline 17APR
#    taskids = [1415974,1416009,1416093,1416090,1417373,1417493,1416608,1390624] # Group 200414
#HieuNguyen     taskids = [1420664] #Group 20200415
#HieuNguyen     taskids = [1414211,1414361,1416225,1417633] # Group 200416

#    directory = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\01_Output_Package\\20200414\\COEM"
#HieuNguyen     directory = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\01_Output_Package\\20200415\\COEM"
    #directory = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\01_Output_Package\\20200416\\COEM"
#    directory = "\\\\hc-ut40346c\\NHI5HC\\hieunguyen\\0000_Project\\001_Prj\\02_JOEM\\01_Output_Package\\20200416\\COEM"
    directory = "\\\\10.184.143.103\\d\\vivi\\BV\\Release\\20200417"

    file_log = open("log_delivery.txt", "w")
    print("Start checker")
    print("*****************************************************************")
    file_log.write("Start checker\n")
    file_log.write("*****************************************************************\n")
    for taskid in taskids:
        data_taskid = doc.get_data(data=data, key="TaskID", value=taskid)
        path_taskid = Path(directory).joinpath(str(taskid) + str("\\RV"))
        #path_taskid = Path(directory).joinpath(str("RV") + str(taskid))
        if (path_taskid.exists()):
            count = 0
            for item in data_taskid.keys():
                function = data_taskid[item].get("ItemName").replace(".c", "")
                user_tester = data_taskid[item].get("Tester")
                b_check_exist = check_exist(directory=path_taskid, function=function)
                if (b_check_exist):
                    count += 1
                    print("{},{},{},{}".format(taskid, function, user_tester, "OK"))
                    file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "OK"))

                else:
                    print("{},{},{},{}".format(taskid, function, user_tester, "NG"))
                    file_log.write("{},{},{},{}\n".format(taskid, function, user_tester, "NG"))

            status = (len(os.listdir(directory + "\\" + str(taskid))) == len(data_taskid)) and (count == len(data_taskid))
            print("## Total {}: status {}: {}/{}/{}".format(str(taskid), status, count, len(os.listdir(path_taskid)), len(data_taskid)))
            print("-----------------------------------------------------------------\n")

            file_log.write("## Total {}: status {}: {}/{}/{}\n".format(str(taskid), status, count, len(os.listdir(path_taskid)), len(data_taskid)))
            file_log.write("-----------------------------------------------------------------\n")



        else:
            print("{} is not existed".format(path_taskid))
            file_log.write("{} is not existed\n".format(path_taskid))
            next

    print("FINISH")
    file_log.write("FINISH\n")
    file_log.close()


if __name__ == "__main__":
    main()
