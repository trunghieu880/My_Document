source /d/workspace/mingw32_env/env.sh

export PATH="$PATH:/c/Users/hieu.nguyen-trung/AppData/Local/Programs/Python/Python37"
alias python37='winpty /c/Users/hieu.nguyen-trung/AppData/Local/Programs/Python/Python37/python.exe'
#---------------------------
# PYTHON
#----------------------------
alias check_jira='winpty /d/workspace/mingw32_env/opt/python-3.8.1/python.exe /d/home/hieunguyen/TUT/PYTHON/filter_logtime.py '
alias python38='winpty /d/workspace/mingw32_env/opt/python-3.8.1/python.exe '
alias homeu='cd /d/home/hieunguyen'
homeu='/d/home/hieunguyen'

alias e='exit'
alias ls='ls --color=auto'
alias l='ls --color=auto -l'
alias ll='ls --color=auto -l'
alias la='ls --color=auto -a'
alias lg='ls | grep --color=always $1'
alias kdiff='/d/Program\ Files/KDiff3/kdiff3.exe' 
#alias xlsx2csv='/d/Program\ Files/Python36/Lib/xlsx2csv.py' 
alias xlsx2csv='/d/workspace/mingw32_env/opt/python-3.8.1/python.exe /c/Python27/Lib/xlsx2csv.py'
xlsx2csv='/d/workspace/mingw32_env/opt/python-3.8.1/python.exe /d/workspace/mingw32_env/opt/python-3.8.1/Lib/xlsx2csv.py' 

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
  
  echo "$mypath" | sed "s|^~|$temp|g" | sed 's|^/||g' | sed 's|/|\\|g' | sed -e 's/^c/c:/g' -e 's/^d/d:/g' -e 's/^u/u:/g';
}
