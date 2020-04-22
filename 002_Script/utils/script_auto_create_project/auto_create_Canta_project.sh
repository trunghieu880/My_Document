#!/bin/bash

source_lib="lib"
script_add_header="./add_header.sh"

sample_project="sample_project"
SOURCE_C_FUNCTION="./Group2"

BUILD_PATH="C:/0000_Prj/002_Working_COEM/20200414/GWM_AB30_CP_Int"

DESTINATION_PATH="./OUTPUT"

function win2linux() {
   echo "$1" | sed -s 's#\\#/#g' | sed -e 's#^D:#/d#g' -e 's#^C:#/c#g'
}

path_linux=`win2linux "$BUILD_PATH"`

function_name="$1"

rm -rf ${DESTINATION_PATH}/${function_name}

echo "CREATE project: $function_name"

cp -rf ./${sample_project} ${DESTINATION_PATH}/${function_name}
cp -rf ./${source_lib}/* ${DESTINATION_PATH}/${function_name}

sed -i "s/sample_project/${function_name}/g" ${DESTINATION_PATH}/${function_name}/.cproject
sed -i "s/sample_project/${function_name}/g" ${DESTINATION_PATH}/${function_name}/.project

sed -i "s@buildPath=\"\w.*${function_name}\"@buildPath=\"${BUILD_PATH}/${function_name}\"@g" ${DESTINATION_PATH}/${function_name}/.cproject

cp -rf ${SOURCE_C_FUNCTION}/${function_name}.c ${DESTINATION_PATH}/${function_name}

list_file_header=`cat ${DESTINATION_PATH}/${function_name}/${function_name}.c  | grep '#include' | grep '\.h' | sed -e 's/^\s*\s//g' -e 's/\s*\s$//g' -e 's/\s*\s/ /g' | sed 's@/\*.*\*/$@@g' | egrep -v '^\/\/|\/\*.*\*/$' | awk '{print $NF}' | sed 's/"//g' | sed 's/\.h$//g'`

echo "CREATE header"
for f in `echo $list_file_header`
do
  ${script_add_header} $f > ${DESTINATION_PATH}/${function_name}/hdr/empty/$f.h
done
