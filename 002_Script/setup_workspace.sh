#! /bin/bash
# Date: Dec-2019
# Author: tai.huu-vo
# Update:
# Setup linux-env on windows OS.
# 	Dependencies:
#		Before you run it, make sure:
#		1. Windows host already has git bash env installed.
#		2. 7zip is installed on C:/Program File/7-zip/
#		3. Network accessible
#		4. Working directory will under D:/workspace.

WORKING_BASE_PATH="/d/workspace"
PYTHON_DOWNLOAD_URL="https://www.python.org/ftp/python/3.8.1/python-3.8.1-embed-amd64.zip"

MINGW_ENV_PATH="${WORKING_BASE_PATH}/mingw32_env"
PYTHON_INSTALL_PATH="${MINGW_ENV_PATH}/opt/python-3.8.1"

PATH="/c/Program Files/7-Zip/:${PATH}"
TOOL_7ZIP="7z.exe"
TOOL_MINGW_GET="mingw-get.exe"

usage() {
	echo "This script supports install linux env on windows machine"
	echo "Just run ${0}"
}

# This function use to install python
install_python() {
    echo "Downloading ${PYTHON_DOWNLOAD_URL}"
    curl ${PYTHON_DOWNLOAD_URL} --out ${MINGW_ENV_PATH}/python-amd64-3.8.1.zip

    mkdir -p ${PYTHON_INSTALL_PATH}/

    mkdir -p ./00_tools/
    ${TOOL_7ZIP} x ${MINGW_ENV_PATH}/python-amd64-3.8.1.zip \
        -o${PYTHON_INSTALL_PATH}/ -r -y

    echo "alias python='winpty ${PYTHON_INSTALL_PATH}/python.exe'" >> ${MINGW_ENV_PATH}/env.sh
    echo "export PATH=\"${PYTHON_INSTALL_PATH}/Scripts/:\$PATH\"" >> ${MINGW_ENV_PATH}/env.sh

    is_update=`cat ${PYTHON_INSTALL_PATH}/python38._pth | grep ".\\Lib\\site-packages"`
    if [[ -z ${is_update} ]]; then
        echo ".\\Lib\\site-packages" >> ${PYTHON_INSTALL_PATH}/python38._pth
    fi

    winpty ${PYTHON_INSTALL_PATH}/python.exe  ./00_tools/get-pip.py
}

main() {
	mkdir -p ${MINGW_ENV_PATH}
	#01. install mingw-get tool
    if [[ ! -f ./00_tools/mingw-get.zip ]]; then
        mkdir -p ./00_tools/
        curl mingw_get_url -out ./00_tools/mingw-get.zip
    fi
	${TOOL_7ZIP} x ./00_tools/mingw-get.zip -o${MINGW_ENV_PATH}/ -r -y

	#02. create env.sh
	echo "export PATH=\"${MINGW_ENV_PATH}/bin/:\$PATH\"" > ${MINGW_ENV_PATH}/env.sh

	#03. install python
	install_python

	#04. update & reload bashrc
	is_update=`cat ~/.bashrc | grep -e "source ${MINGW_ENV_PATH}/env.sh"`
	if [[ -z $is_update ]]; then
		echo "source ${MINGW_ENV_PATH}/env.sh" >> ~/.bashrc
	fi
	source ~/.bashrc

	#05. install some usefull packages
	#echo $PATH
	${TOOL_MINGW_GET} install gcc g++ mingw32-make gdb mingw32-pthreads-w32 \
        	msys-perl
	# create symbol link mingw32-make alias make
	ln -s  ${MINGW_ENV_PATH}/bin/mingw32-make.exe  ${MINGW_ENV_PATH}/bin/make

	echo "All done, run: source ~/.bashrc to update PATH env"
}

# main entry.
main $@
# End.

