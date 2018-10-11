#!/bin/bash

rm -f _current_test.dl
cp $1 _current_test.dl
mkdir -p ./out

if [ $? -ne 0 ] ; then
	echo "No such file: $1, aborting run"
	exit -1
fi

souffle ty_dsa.dl -D- --verbose && souffle ty_dsa.dl -D./out --verbose >/dev/null 2>&1

