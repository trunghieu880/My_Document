#!/bin/bash
##HieuNguyen set -x
LOG_INPUT="$1"

if [ ! -e "$LOG_INPUT" ]
then
   echo "File $LOG_INPUT: is not exist"
   exit 1
else
   if [ "`basename $LOG_INPUT`" != "test_log.json" ]
   then
       echo "Please specify to the test_log.json"
       exit 1
   fi
fi

printf "%0.s-" {1..170}
printf "\n"
printf "%-90s | %-20s | %-20s | %-20s | %-20s\n" "PAT_TEST_NAME" "NUM_SUBTESTS" "NUM_SUBTEST_PASS" "NUM_SUBTEST_FAIL" "STATUS"
printf "%0.s-" {1..170}
printf "\n"

for temp_pat in `grep '"test"' $LOG_INPUT | sed 's/^\s\+//g' | sed 's/"//g' | sed 's/\s\+/ /g' | sed 's/,$//g' | awk '{print $NF}'`
do
   pat_test_name="`basename "$temp_pat"`"
   sed -n '/^    {/,/^    }/p' $LOG_INPUT | sed -n "/\"test\": .*\/${pat_test_name}\>/,/^    }/p" | sed '1 i INSERT{' | sed 's/INSERT{/    {/g' > temp_${pat_test_name}

   num_subtests=`sed -n '/"subtests": \[/,/      \]/p' ./temp_${pat_test_name} | grep -c '"name":'`
   num_subpass=`sed -n '/"subtests": \[/,/      \]/p' ./temp_${pat_test_name} | grep '"status":' | grep -c '"PASS"'`
   num_subfail=`sed -n '/"subtests": \[/,/      \]/p' ./temp_${pat_test_name} | grep '"status":' | grep -c '"FAIL"'`
   num_subfail=`sed -n '/"subtests": \[/,/      \]/p' ./temp_${pat_test_name} | grep '"status":' | grep -c '"FAIL"'`
   status=`grep -A 1 '],$' ./temp_${pat_test_name} | grep '"status"' | sed -e 's/"//g' -e 's/,//g' | awk '{print $NF}'`

   printf "%-90s | %-20s | %-20s | %-20s | %-20s\n" "$pat_test_name" $num_subtests $num_subpass $num_subfail $status
#   printf "%-90s | %-20s | %-20s | %-20s | %-20s\n" "$pat_test_name" "?" "?" "?" "?"

   rm -rf ./temp_${pat_test_name}
done

