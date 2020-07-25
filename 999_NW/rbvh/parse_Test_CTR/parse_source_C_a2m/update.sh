#!/bin/bash

echo "COPY ASSETS"

list="assets main.sh"
new_path="`find ./dist -mindepth 1 -maxdepth 1`"

for f in `echo $list`
do
	echo "Copy file: $f"
	cp -ruv $f ${new_path}
done
