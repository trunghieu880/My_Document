#!/bin/bash

user=`whoami`
input="$1"
date_now=`date "+%b %d, %Y"`
cat << EOF
/*
 * ${input}.h
 *
 *  Created on: ${date_now}
 *      Author: ${user}
 */

#ifndef HDR_${input^^}_H_
#define HDR_${input^^}_H_


#include "include.h"

#endif /* HDR_${input^^}_H_ */
EOF

