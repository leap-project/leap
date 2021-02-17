#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[ip_file_path]"
    exit
fi

filepath=$1
echo "Killing cloud"
for line in $(cat $filepath);do
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
	echo "killing" $hostname
	ssh stolet@$hostname 'pkill -f coordinator-main'
	ssh stolet@$hostname 'pkill -f cloudalgo_main'
done
