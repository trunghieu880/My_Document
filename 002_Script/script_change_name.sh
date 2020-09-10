#!/bin/bash

old_name="$1"
new_name="$2"

if [ "${old_name}" == "" ]
then
    echo "Please input your pattern"
    exit 0
fi

for f in `ls | grep "${old_name}"`
do
    file_new_name=`echo "$f" | sed "s/${old_name}/${new_name}/g"`
    echo "$f $file_new_name"
    mv -f ${f} ${file_new_name}
done
