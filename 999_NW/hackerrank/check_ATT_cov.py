import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import re

logger = logging.getLogger(__name__)

def scan_files(directory, ext='.txt'):
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

def get_infor_cov(path):
    '''Check source code is Simulink model'''
    try:
        flag_count = 0

        data = dict()
        with open(path, encoding='shift-jis', errors='ignore') as fp:
            for line in fp.readlines()[:100]:
                line = line.strip()
                if flag_count > 1:
                    break

                if '---------------------------------------------------------' in line:
                    flag_count = flag_count + 1
                    next
                if (flag_count == 1):
                    if 'Statement blocks' in line or 'Decisions' in line or 'Modified conditions' in line:
                        temp = re.sub("\s+\.+\s+", ":", line)
                        temp = re.sub("%\s\(.*\)$", "", temp)
                        
                        key = temp.split(":")[0]
                        val = temp.split(":")[1]
                        if key == "Statement blocks":
                            key = "C0"
                        elif key == "Decisions":
                            key = 'C1'
                        elif key == "Modified conditions":
                            key = 'MCDC'
                            rst = True

                        data = {**data, key : val}

    except:
        data = {}
    finally:
        return data

def main():
    directory = "C:\\Users\\hieu.nguyen-trung\\Desktop\\Test_Folder\\Output_ATT"
    data = scan_files(directory, ext='ReportRTRT.txt')
    for f in data[0]:
        new_file = Path(f.parent, 'ReportRTRT.txt')
        print(get_infor_cov(new_file))

main()