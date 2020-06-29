#!/bin/bash

input="$1"

if [ ${input} -eq 1 ]
then
    echo "Updating index"
    sh ./script_convert_index.sh
elif [ ${input} -eq 2 ]
then
    echo "Convert auto to manual"
    sh ./script_convert_auto2manual.sh
else
    echo "Updating index and convert auto to manual"
    sh ./script_convert_index.sh
    sh ./script_convert_auto2manual.sh
fi
