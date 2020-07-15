import json
import logging
import os
import sys
import utils
from datetime import datetime
from pathlib import Path
import time

import re
import subprocess

logger = logging.getLogger(__name__)

ASSET = Path(__file__).parent.joinpath('assets')
SETTING = ASSET.joinpath('settings.json')

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
        data = dict()
        result = dict()

        pattern_start = 'void ' + str(tc_name) + "(int doIt){"
        pattern_end = 'END_TEST();'
        with open(path, encoding='shift-jis', errors='ignore') as fp:
            old = ""
            new = ""
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
                        temp = line
                        if(re.search('"[0-9]+[:_]', temp) != None):
                            temp = re.sub('"[0-9]+:', '"' + str(index) + ":", temp)
                            temp = re.sub('"[0-9]+: ', '"' + str(index) + ": ", temp)
                            temp = re.sub('"[0-9]+_', '"' + str(index) + ": ", temp)
                        else:
                            temp = re.sub('"(.*)"', '"{}: {}"'.format(str(index), r'\1'), temp)

                        temp = re.sub('_\d+",', '",', temp)

                        if "test_" in temp:
                            temp = re.sub('(\d+): (test_){1,}(\w.*)",', r'\1: test_\3_\1",', temp)
                        else:
                            temp = re.sub('(\d+): (\w.*)",', r'\1: test_\2_\1",', temp)

                        old = re.sub('^.*\("', '', line)
                        old = re.sub('".*$', '', old)

                        new = re.sub('^.*\("', '', temp)
                        new = re.sub('".*$', '', new)

                        # subprocess.call(['sed', '-i', 's@{}@{}@g'.format(line, temp), "'{}'".format(path.as_posix())])

                        function_name = re.sub('(\d+): (.*)', r'\2', new)
                        old_function = str(tc_name) + "("
                        new_function = function_name + "("

                        with open("./script_convert_index.sh", errors='ignore', mode='a') as f:
                            f.write("sed -i 's@{}@{}@g' {}\n".format(line, temp, "'{}'".format(path.as_posix())))

                        with open("./script_convert_auto2manual.sh", errors='ignore', mode='a') as f:
                            f.write("sed -i 's@{}@{}@g' {}\n".format(old_function, new_function, "'{}'".format(path.as_posix())))
                    else:
                        if(re.search('^"(\w.*)"\);$', line) or re.search('^"<(\w.*)>"\);$', line)):
                            description = re.sub('^"(.*)"\);$', r'"\1"', line)
                            result[tc_name] = {**data, tc_name: '"{}" -> "{}"'.format(old, new), "description": description}
    finally:
        return result

def get_list_testcase_c(path):
    l_tc = []
    flag_start_test = False
    with open(path, encoding='shift-jis', errors='ignore') as fp:
        for line in fp.readlines():
            line = line.strip()

            pattern_start = '/* Prototypes for test functions */'
            pattern_end = '/*****************************************************************************/'
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
    print("***********************************")
    print("PRINT INFOR")
    print("***********************************\n")
    for item in l_d:
        for child_key in item.keys():
            print("-----------------------------------")
            print("Test case name: %s" % child_key)
            print("-----------------------------------")
            for key in item[child_key].keys():
                val = item[child_key][key]
                print('{}'.format(val))

        print("***********************************\n")

def update_comment(path, l_d):
    print("***********************************")
    print("UPDATE COMMENT")
    print("***********************************\n")

    with open(path, encoding='shift-jis', errors='ignore') as fp:
        flag_start_test = False
        flag_start_collect = False
        index_tc = -1

        pattern_start = '(\*){1,}TC_'
        pattern_end = '(\-){1,}(\*){1,}'

        with open("./temp.c", errors='ignore', mode='a') as f:
            for line in fp.readlines():
                if re.search('^{}'.format(pattern_start), line):
                    index_tc = int(re.sub("^.*TC_(\d+).*", r'\1', line)) - 1
                    flag_start_test = True

                if re.search('^' + pattern_end + "$", line):
                    flag_start_test = False

                if (flag_start_test):
                    if '---- Test goal:' in line:
                        f.write(line)
                        for child_key in l_d[index_tc].keys():
                            print("Test case name: %s" % child_key)
                            print(l_d[index_tc][child_key]["description"])
                            for cmt in l_d[index_tc][child_key]["description"].split(";"):
                                f.write("{}- {}\n".format(" "*12, cmt.strip()))
                    else:
                        if re.search('^Check the code coverage.$', line.strip()):
                            next
                        else:
                            f.write(line)
                else:
                    f.write(line)

    print("-----------------------------------")
    print("Please get your output at: {}".format("./temp.c"))
    print("-----------------------------------")

def main():
    directory = utils.load(SETTING).get("directory")
    opt = utils.load(SETTING).get("option")

    data = scan_files(directory, ext='.c')

    if Path("./script_convert_auto2manual.sh").exists():
        os.remove("./script_convert_auto2manual.sh")
    if Path("./script_convert_index.sh").exists():
        os.remove("./script_convert_index.sh")

    if Path("./temp.c").exists():
        os.remove("./temp.c")

    l_d = list()
    for f in data[0]:
        new_file = Path(f.parent, f.name)
        l_tc = get_list_testcase_c(new_file)

        with open("./script_convert_auto2manual.sh", errors='ignore', mode='a') as f:
            f.write("sed -i '/^\s*\sIF_INSTANCE/,/}/{/CHECK.*/d;};' " + "'" + new_file.as_posix() + "'\n")
            f.write("sed -i -e 's/85U/0xAA/g' " + "'" + new_file.as_posix() + "'\n")
            f.write("sed -i -e 's/default case/<Insert test case description here>/g' -e 's/created to.*\"/<Insert test case description here>\"/g' -e 's|\s\+/\* Generated by Cantata \*/||g' " + "'" + new_file.as_posix() + "'\n")

        if(len(l_tc) > 0):
            for index, tc in enumerate(l_tc):
                l_d.append(get_infor_c(new_file, tc, index + 1))

            print_infor_c(l_d)
            # update_comment(path=new_file, l_d=l_d)
        else:
            print("Not found TEST CASE in LOG FILE")

    print("-----------------------------------")
    print("NEXT STEP: YOUR OPTION is {}".format(opt))
    print("-----------------------------------")
    print('./main.sh <option>\n' \
          '  with:\n' \
          '    + option = 1: update index of testcase\n'\
          '    + option = 2: convert auto to manual\n'\
          '    + option = other: update index & convert auto to manual\n')

    os.system('main.sh ' + str(opt))

    if Path("./script_convert_auto2manual.sh").exists():
        os.remove("./script_convert_auto2manual.sh")
    if Path("./script_convert_index.sh").exists():
        os.remove("./script_convert_index.sh")

    os.system("pause")

main()
