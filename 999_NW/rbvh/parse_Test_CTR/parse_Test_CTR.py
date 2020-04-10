import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import re

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
        data = dict()
        result = dict()
        key = ""
        val = ""

        pattern_start = 'Start Test: ' + str(tc_index)
        pattern_end = 'End Test: ' + str(tc_index)
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
                    if '>> FAILED' in line:
                        flag_start_collect = True
                        temp = re.sub("^>> FAILED: Check ", "", line)
                        key = temp.split("=")[1].strip()
                        
                    if (flag_start_collect):
                        if 'actual:' in line:
                            val = line.split(":")[1].strip()
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
    with open(path, encoding='shift-jis', errors='ignore') as fp:
        for line in fp.readlines():
            line = line.strip()
            if 'Start Test: ' in line:
                temp = "^.*" + 'Start Test: '
                temp = re.sub(temp, "", line).strip()
                tc_index = re.sub(":.*$", "", temp).strip()
                l_tc.append(tc_index)
    
    return l_tc

def print_infor(l_d):
    for item in l_d:
        for child_key in item.keys():
            print("-----------------------------------")
            print("Test case name: %s" % child_key)
            print("-----------------------------------")
            for key in item[child_key].keys():
                val = item[child_key][key]
                print("%s = %s;" % (key, val))



def main():
    directory = "C:\\Users\\hieu.nguyen-trung\\Desktop\\Test_Folder"
    data = scan_files(directory, ext='.ctr')

    for f in data[0]:
        new_file = Path(f.parent, f.name)
        l_tc = get_list_testcase(new_file)

        if(len(l_tc) > 0):
            l_d = []
            for i in l_tc:
                l_d.append(get_infor_ctr(new_file, i))
            
            print_infor(l_d)
        else:
            print("Not found TEST CASE in LOG FILE")

main()