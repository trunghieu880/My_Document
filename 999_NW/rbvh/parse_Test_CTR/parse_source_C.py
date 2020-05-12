import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import re
import subprocess

logger = logging.getLogger(__name__)

def scan_files(directory, ext='.c'):
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

def get_infor_c(path, tc_name="test_1", index=1):
    try:
        flag_start_test = False
        flag_start_collect = False
        flag_start_access = False
        data = dict()
        result = dict()
        key = ""
        val = ""

        pattern_start = 'void ' + str(tc_name) + "(int doIt){"
        pattern_end = 'END_TEST();'
        with open(path, encoding='shift-jis', errors='ignore') as fp:
            for line in fp.readlines():
                line = line.strip()

                if pattern_start in line:
                    flag_start_test = True
                    result[tc_name] = {**data}
                    next
                if pattern_end in line:
                    flag_start_test = False
                    next
                if (flag_start_test):
                    if 'START_TEST' in line:
                        temp = re.sub("[0-9]+:", str(index) + ":", line)
                        temp = re.sub("[0-9]+: ", str(index) + ": ", temp)
                        temp = re.sub("[0-9]+_", str(index) + ": ", temp)

                        old = re.sub('^.*\("', '', line)
                        old = re.sub('".*$', '', old)

                        new = re.sub('^.*\("', '', temp)
                        new = re.sub('".*$', '', new)
                        result[tc_name] = {**data, tc_name: '"{}" -> "{}"'.format(old, new)}
                        
                        subprocess.call(['sed', '-i', 's@{}@{}@g'.format(line, temp), "'{}'".format(path.as_posix())])

                        # with open("./script.sh", errors='ignore', mode='a') as f:
                            # f.write("sed -i 's@{}@{}@g' {}\n".format(line, temp, "'{}'".format(path.as_posix())))

    finally:
        return result

def get_list_testcase_c(path):
    l_tc = []
    flag_start_test = False
    with open(path, encoding='shift-jis', errors='ignore') as fp:
        for line in fp.readlines():
            line = line.strip()

            pattern_start = '/* Prototypes for test functions */'
            pattern_end = '/*******************************************/'
            if pattern_start in line:
                flag_start_test = True
                next
            if flag_start_test and pattern_end in line:
                flag_start_test = False
                next
            if (flag_start_test):
                if 'void test_' in line:
                    str_tc = re.sub("^.*void\s+", "", line)
                    str_tc = re.sub("\(.*$", "", str_tc)

                    l_tc.append(str_tc)
                    next

    return l_tc

def print_infor_c(l_d):
    for item in l_d:
        for child_key in item.keys():
            print("-----------------------------------")
            print("Test case name: %s" % child_key)
            print("-----------------------------------")
            for key in item[child_key].keys():
                val = item[child_key][key]
                print('{};'.format(val))

        print("***********************************\n")

def main():
    directory = "C:\\Users\\hieu.nguyen-trung\\Desktop\\Test_Folder"
    # directory = "C:\\0000_Prj\\002_Working_COEM\\20200507\\COEM\\OUTPUT\\RBAPLEOL_ValvesToggling\\Cantata\\tests\\atest_RBAPLEOL_ValvesToggling_3"
    data = scan_files(directory, ext='.c')
    # os.remove("./script.sh")
    for f in data[0]:
        new_file = Path(f.parent, f.name)
        l_tc = get_list_testcase_c(new_file)
        # l_tc = ["test_1"]
        print(l_tc)

        if(len(l_tc) > 0):
            l_d = []
            for index, tc in enumerate(l_tc):
                l_d.append(get_infor_c(new_file, tc, index + 100))

            print_infor_c(l_d)
        else:
            print("Not found TEST CASE in LOG FILE")

main()
