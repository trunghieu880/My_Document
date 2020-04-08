#----------------------------
# PYTHON
#----------------------------
alias python27='winpty /c/Python27/python.exe ' 
alias python37='winpty /c/Python37/python.exe'

alias homeu='cd /c/Users/NHI5HC/Desktop/home/hieunguyen'
homeu='/c/Users/NHI5HC/Desktop/home/hieunguyen'

alias e='exit'
alias ls='ls --color=auto'
alias l='ls --color=auto -l'
alias ll='ls --color=auto -l'
alias la='ls --color=auto -a'
alias lg='ls | grep --color=always $1'
alias kdiff='~/Desktop/home/hieunguyen/utils/KDiff3-0.9.92/kdiff3.exe'
alias tree='~/Desktop/home/hieunguyen/utils/tree.exe'

alias auto_zip="/c/Users/NHI5HC/Desktop/home/hieunguyen/Material_HieuNguyen/My_Document/002_Script/utils/auto_zip.sh "
auto_zip="/c/Users/NHI5HC/Desktop/home/hieunguyen/Material_HieuNguyen/My_Document/002_Script/utils/auto_zip.sh "

alias auto_unzip="/c/Users/NHI5HC/Desktop/home/hieunguyen/Material_HieuNguyen/My_Document/002_Script/utils/auto_unzip.sh "
auto_unzip="/c/Users/NHI5HC/Desktop/home/hieunguyen/Material_HieuNguyen/My_Document/002_Script/utils/auto_unzip.sh "

alias xlsx2csv='/c/Python27/python.exe /c/Python27/Lib/site-packages/xlsx2csv.py'
xlsx2csv='/c/Python27/Lib/site-packages/xlsx2csv.py'
alias xls2csv='/c/Python27/python.exe /c/Python27/Lib/site-packages/xls2csv.py'
xls2csv='/c/Python27/Lib/site-packages/xls2csv.py'


# Make and change directory at once
alias mkcd='_(){ mkdir -p $1; cd $1; }; _'

# fast find
alias ff='find . -name $1'

# change directories easily
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'

alias grepc='grep --color=always'
alias egrepc='egrep --color=always'
alias fgrepc='fgrep --color=always'
alias h='history'
alias rmf='rm -rf'
alias cpf='cp -rf'
alias b='cd -'
alias c='clear'

alias path='echo -e ${PATH//:/\\n}'
alias now='date +"%T"'
alias nowtime='now'
alias nowdate='date +"%d-%m-%Y"'
alias vi=vim

#12: Show open ports
alias ports='netstat -tulanp'

alias df='df -H'
alias du='du -ch'

# Tar and compress (and untar) all those fastq, csv, vcf, and other files
# create .tar.gz 
function targz() { tar -zcvf $1.tar.gz $1; rm -r $1; }
# extra .tar.gz
function untargz() { tar -zxvf $1; rm -r $1; }

# Count number of files in a directory
function numfiles() { 
  N="$(ls $1 | wc -l)";

  if [ "$1" != "" ]; then
    echo "$N files in $1";
  else
    echo "$N files in `pwd`";
  fi
}

function win() {
  temp=`echo ~`
  mypath=""
  if [ "$1" != "" ]; then
    mypath="$1"
  else
    mypath=`pwd`
  fi
  
  echo "$mypath" | sed "s|^~|$temp|g" | sed 's|^/||g' | sed 's|/|\\|g' | sed 's/^c/c:/g' | sed 's/^d/d:/g' | sed 's|^\\hc-ut40346c|\\\\hc-ut40346c|g';
}

function win2linux() {
  echo "$1" | sed -s 's#\\#/#g' | sed -e 's#^D:#/d#g' -e 's#^C:#/c#g'
}

function trim_input(){
  if [ "$1" != "" ]; then
    grep -i -e '</\?TABLE\|</\?TD\|</\?TR\|</\?TH' $1 | sed 's/^[\ \t]*//g' | tr -d '\n' | sed 's/<\/TR[^>]*>/\n/Ig' \
      | sed 's/^<T[DH][^>]*>\|<\/\?T[DH][^>]*>$//Ig' | sed 's/<\/T[DH][^>]*><T[DH][^>]*>/,/Ig' \
      | head -4 | tail -n -2 | egrep '>Variable&nbsp;Name,|>Type,' | sed -e 's/<TR><TD .*>Variable&nbsp;Name,//g' -e 's/<TR><TD .*>Type,//g' -e 's/<BR>//g' -e 's/&nbsp;/ /g' \
      | sed 's/,\w\+\.c\//,/g' \
      | tac | awk -F, '{for (f=1;f<=NF;f++) col[f] = col[f]":"$f} END {for (f=1;f<=NF;f++) print col[f]}' | tr ':' ' ' | sed 's/^\s*\s//g'

  else
    echo "Please insert exel path"
  fi
}

function get_data_ATT(){
  cat $1 | sed -n '/<OutputSignals>/,/<\/OutputSignals>/p' | sed -e 's|<\!\[CDATA\[||g' -e 's|\]||g' | egrep -v 'SignalName|SignalVerdict|Time|Expected|Tolerance' | sed '/SignalDetail.*$/d' | sed 's/<Signal>//g' | sed 's/><\/Signal>//g' | sed 's/\s\+//g' | tr '\n' ',' | sed 's/<\/\w\+>,/\n/g' | sed 's/<\w\+>//g' | sed 's/^,//g' | sed 's/,$//g' | sed 's/,/ /g'
}

function gen_id () { 
  FILE_SUMMARY="//hc-ut40346c/NHI5HC/hieunguyen/0000_Project/001_Prj/02_JOEM/Summary_JOEM.xlsm" 
  PRJ_FINDING="CW10_EMP2V3_SmartCar_MHEV_381" 
  userid="hieu.nguyen-trung" 
  itemnumber=$1 
  /c/Python27/python.exe /c/Python27/Lib/site-packages/xlsx2csv.py -s 1 ${FILE_SUMMARY}  | sed 's/^,//g' | sed -n '/^No,Package/,/^Table KPI ASW/p' | grep '^[0-9]\+,' | grep ${PRJ_FINDING} | grep "$userid" | awk -F, '{printf "%s,%s,%s,%s,%s\n", $1, $4, $6, $7, $11}' | sed 's/MT_//g' | grep "^${itemnumber}" | awk -F, '{printf "module_name = \"%s\"\nmodule_version = \"%s\"\nmodule_number = \"%s\"\n", $4, $NF, $3}'
} 

###############################
user="hieunguyen"
pc_id="NHI5HC"
link_share_hieunguyen="//hc-ut40346c/${pc_id}"
share_folder_hieunguyen="/c/TSDE_Workarea/${pc_id}"

prj_coem="$link_share_hieunguyen/${user}/0000_Project/001_Prj/01_COEM"
prj_joem="$link_share_hieunguyen/${user}/0000_Project/001_Prj/02_JOEM"

database_ATT="/c/TSDE_Workarea/ETASData/ASCET/V6_1_4/ATT"
working_folder="/c/0000_Prj/000_Working_Folder"

release_package_PSA_PHEVv1_81ASW_10PSW="//hc-ut40346c/NHI5HC/hieunguyen/0000_Project/001_Prj/02_JOEM/02_Release_Package/20200305/PSA_PHEVv1_81ASW_10PSW/T500"
