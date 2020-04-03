#!/bin/bash

your_test_design="$1"

path_ATT_project='~/Desktop/Test_Folder'

func_name=`dirname $your_test_design | awk -F/ '{print $NF}' | sed -e 's/^TD_//g' -e 's/_v[0-9]_.*\.xls$/\.xls/g'`


cd `basename $your_test_design`

cp -uv $path_ATT_project/$func_name
