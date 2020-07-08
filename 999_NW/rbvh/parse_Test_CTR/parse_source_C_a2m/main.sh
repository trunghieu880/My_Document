#!/bin/bash

input="$1"

if [ ${input} -eq 1 ]
then
    echo "Updating index"
    tac ./script_convert_index.sh > ~/.temp.sh
    sh ~/.temp.sh
    rm ~/.temp.sh
elif [ ${input} -eq 2 ]
then
    echo "Convert auto to manual"
    tac ./script_convert_auto2manual.sh > ~/.temp.sh
    sh ~/.temp.sh
    rm ~/.temp.sh
else
    echo "Updating index and convert auto to manual"
    tac ./script_convert_index.sh > ~/.temp.sh
    sh ~/.temp.sh
    rm ~/.temp.sh
    tac ./script_convert_auto2manual.sh > ~/.temp.sh
    sh ~/.temp.sh
    rm ~/.temp.sh
fi
