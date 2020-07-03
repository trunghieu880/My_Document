import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import re
import subprocess


logger = logging.getLogger(__name__)

def scan_files(directory, ext='.ctr'):
    '''Scan all file that has extension in directory'''
    logger.debug("Scan directory %s %s", directory, ext)
    data = []
    latest = None
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(ext):
                filepath = Path(root).joinpath(filename)
                data.append(filepath)

                if (latest is None or
                        Path(latest).stat().st_mtime < filepath.stat().st_mtime):
                    latest = filepath

    return data, latest

def get_infor_ctr(path, tc_index=1):
    try:
        flag_start_test = False
        flag_start_collect = False
        flag_start_access = False
        data = dict()
        result = dict()
        key = ""
        val = ""

        pattern_start = 'Start Test: ' + str(tc_index) + ":"
        pattern_end = 'End Test: ' + str(tc_index) + ":"
        with open(path, encoding='shift-jis', errors='ignore') as fp:
            for line in fp.readlines():
                line = line.strip()

                if pattern_start in line:
                    flag_start_test = True
                    temp = "^.*" + 'Start Test: '
                    tc_name = re.sub(temp, "", line).strip()
                    result[tc_name] = {**data}
                    next
                if pattern_end in line:
                    flag_start_test = False
                    next
                if (flag_start_test):
                    if '>>  FAILED' in line:
                        if 'Check:' in line or 'Check Memory:' in line:
                            flag_start_collect = True
                            if 'Check:' in line:
                                temp = re.sub("^>>.*Check: ", "", line)
                                if re.search("ACCESS_VARIABLE", line):
                                    flag_start_access = True
                                    key = temp
                                elif re.search("=$", line):
                                    key = temp.split("=")[0].strip()
                                else:
                                    key = temp.split("=")[1].strip()

                            elif 'Check Memory:':
                                temp = re.sub("^>>.*Check Memory: ", "", line)
                                key = temp.strip()

                            if re.search("ACCESS_VARIABLE", line):
                                key = re.sub("ACCESS_VARIABLE", "ACCESS_EXPECTED_VARIABLE", key)
                            elif not re.search('^expected_', key):
                                key = "expected_" + key
                            else:
                                continue
                        else:
                            if 'No match for' in line:
                                temp = re.sub("^>>.*for ", "", line)
                                temp = re.sub(" in expected.*$", "", temp)
                                data = {**data, temp : "#default"}
                                continue
                            else:
                                print("BUG check: Not find No match for")

                    if (flag_start_collect):
                        if flag_start_access:
                            if re.search("=$", line):
                                key = key + " " + line.split("=")[0].strip()
                                flag_start_access = False

                        if 'actual:' in line:
                            temp = re.sub("\s*\s<.*>$", "", line)
                            temp = re.sub("\s*\s", " ", temp)
                            temp = re.sub("\s*\s\'.*$", " ", temp)
                            val = temp.split(":")[1].strip()
                            data = {**data, key : val}
                            key = ""
                            val = ""
                            flag_start_collect = False
                            next
        result[tc_name] = {**data}
    except:
        result = {}
    finally:
        return result

def get_list_testcase(path):
    l_tc = []
    flag_start_test = False
    tc_index = -1
    with open(path, encoding='shift-jis', errors='ignore') as fp:
        for line in fp.readlines():
            line = line.strip()

            pattern_start = 'Start Test: '
            pattern_end = 'End Test: '
            if pattern_start in line:
                flag_start_test = True
                temp = "^.*" + 'Start Test: '
                temp = re.sub(temp, "", line).strip()
                tc_index = re.sub(":.*$", "", temp).strip()
                next
            if pattern_end in line:
                flag_start_test = False
                next
            if (flag_start_test):
                if '>>  FAILED' in line:
                    l_tc.append(tc_index)
                    flag_start_test = False
                    next

    return l_tc

def print_infor(l_d):
    for item in l_d:
        for child_key in item.keys():
            print("-----------------------------------")
            print("Test case name: %s" % child_key)
            print("-----------------------------------")
            for key in item[child_key].keys():
                val = item[child_key][key]
                subprocess.call(['sed', '-i', '/START_TEST("{}/i\\\t{} = {};'.format(child_key, key, val), 'C:/Users/nhi5hc/Desktop/Test_Ctr/src.c'])

                print("%s = %s;" % (key, val))

        print("***********************************\n")

def main():
    # directory = "C:\\Users\\hieu.nguyen-trung\\Desktop\\Test_Folder"
    directory = "C:\\Users\\nhi5hc\\Desktop\\Test_Ctr"
    # directory = "C:\\0000_Prj\\002_Working_COEM\\20200507\\COEM\\OUTPUT\\RBAPLEOL_ValvesToggling\\Cantata\\tests\\atest_RBAPLEOL_ValvesToggling_3"
    data = scan_files(directory, ext='.ctr')
    
    # subprocess.call(['sed', '-i', '/^\s*\sinitialise_expected_global_data/,/START_TEST/\{//!d;\};', 'C:/Users/nhi5hc/Desktop/Test_Ctr/test.c'])
    for f in data[0]:
        new_file = Path(f.parent, f.name)
        l_tc = get_list_testcase(new_file)
        # l_tc = [16]

        if(len(l_tc) > 0):
            l_d = []
            for i in l_tc:
                flag_found_fail = False
                l_d.append(get_infor_ctr(new_file, i))

            print_infor(l_d)
        else:
            print("Not found TEST CASE in LOG FILE")

main()
