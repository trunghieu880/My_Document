#!/bin/bash -x

#HieuNguyen set +x
you_want_create_list_database_again="NO"
#HieuNguyen you_want_create_list_database_again="NO"

you_want_update_list_check_again="YES"

#Create your list finding from database
your_input_path="$1"

XLSX2CSV="/c/Python27/python.exe /c/Python27/Lib/site-packages/xlsx2csv.py "
SUMMARY="//hc-ut40346c/NHI5HC/hieunguyen/0000_Project/001_Prj/02_JOEM/Summary_JOEM.xlsm"

str_ignore="src_tpl|Unit_tst|Unit_test|Test_Script|Unit Test"

if [ "${you_want_update_list_check_again}" == "YES" ]
then
  echo "CREATE LIST CHECK AGAIN"
  ${XLSX2CSV} -s 1 ${SUMMARY} | sed -n '/^,No,Package/,/^,Table KPI ASW/p' | egrep -v '^,\+$' | sed 's/^,\+//g' > .TEMP_SUMMARY

  COL_No=`grep "^No," .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "No") {print i; break}; i++}}'`
  COL_ComponentName=`grep "^No," .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "ComponentName") {print i; break}; i++}}'`
  COL_ItemName=`grep "^No," .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "ItemName") {print i; break}; i++}}'`
  COL_Database=`grep "^No," .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Database") {print i; break}; i++}}'`
  COL_Tester=`grep "^No," .TEMP_SUMMARY | awk -F, '{i = 1; while ( i <= NF ) { if ($i == "Tester") {print i; break}; i++}}'`

  grep '^[0-9]\+,' .TEMP_SUMMARY \
    | grep -v '^,No,' \
    | awk -v col_no=$COL_No -v col_componentname=$COL_ComponentName -v col_itemname=$COL_ItemName -v col_database=$COL_Database -v col_tester=$COL_Tester \
          -F, '{printf "%s,%s,%s,%s\n", \
               $col_no, $col_componentname, $col_itemname, $col_database}' \
    | sed 's|\\|/|g' | grep -v ',*,$' > ./LIST
fi

if [ "${you_want_create_list_database_again}" == "YES" ]
then
  echo "CREATE LIST AGAIN"
  if [ -n "$your_input_path" ]
  then
    if [ -e ${your_input_path} ]
    then
      for item in `ls ${your_input_path} | egrep -v '\.zip$|\.sh$'`
      do
        echo "Create database ${item}"
        find ${your_input_path}/${item} > ./list_${item}
      done
    else
      echo "${your_input_path} is not existed"
      exit 1
    fi
  else
    echo "Please put your link"
    exit 2
  fi
fi

for line in `cat ./LIST | sed 's/\.zip//g' | grep -v '^#'`
do

  item_index=`echo "$line" | awk -F, '{print $1}'`
  path_c=`echo "$line" | awk -F, '{print $2}'`
  source_c=`echo "$line" | awk -F, '{print $3}'`
  database=`echo "$line" | awk -F, '{print $4}'`

  if [ -e list_${database} ]
  then
    num_check=`grep "${source_c}$" ./list_${database} | egrep -vic "${str_ignore}"`
    data_find="`grep "${source_c}$" ./list_${database} | egrep -vi "${str_ignore}"`"

    if [ $num_check -gt 0 ]
    then
      num_check_path=`echo "${data_find}" | grep -v "$data_base/\." | grep -c "/${path_c}/" |  egrep -vi "${str_ignore}"`
      if [ $num_check_path -eq 1 ]
      then
         data_find="`echo "${data_find}" | grep -v "$database/\." | grep "/$path_c/" | egrep -vi "${str_ignore}"`"
         num_check=$num_check_path
         echo "************************************"
         echo "$item_index - $source_c - ${database} : $num_check : OK : ${data_find}"
         echo "************************************"
      else
         echo "************************************"
         echo "$item_index - $source_c - ${database} : $num_check : NG : ${data_find}"
         echo "************************************"
      fi
    else
      echo "************************************"
      echo "$item_index - $source_c - ${database} : $num_check : NG : NOT FOUND"
      echo "************************************"
    fi
  else
    echo "************************************"
    echo "$item_index - $source_c - ${database} : not found database"
    echo "************************************"
  fi

  echo "-------------------------------------------------------------"
done

