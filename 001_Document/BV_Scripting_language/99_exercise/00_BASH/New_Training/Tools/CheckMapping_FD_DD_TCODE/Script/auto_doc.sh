#!/usr/bin/sh

work=$PWD
base_dir=`dirname $0`
config_file=`ls $work/../docs/sds/*Configuration.xlsx`
error_list_file=`ls $work/../docs/sds/*GenTool_ErrorList.xlsx`
detail_design_file=`ls $work/../docs/sds/*GenTool_DD.docx`
check_mapping_result=$base_dir/check_mapping_result.py

source_code_path="SpiX1x\\"
module_specific="SPI_GDD_CLS_\d+_\d+"

# Check file exist
if [[ -f $config_file ]] && [ -f $error_list_file ] && [ -f $detail_design_file ]; then
    $check_mapping_result $module_specific $config_file $error_list_file $detail_design_file $source_code_path $base_dir
fi
