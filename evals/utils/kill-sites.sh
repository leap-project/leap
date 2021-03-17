#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[ip_file_path, num_sites]"
    exit
fi

filepath=$1
n_sites=$2

echo "Killing sites"

i=1
for line in $(cat $filepath);do
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
	echo "killing" $hostname
	ssh stolet@$hostname 'pkill -f connector-main'
	ssh stolet@$hostname 'pkill -f sitealgo_main'

  if [ $i -eq $n_sites ]; then
    break
  fi
  i=$((i + 1))
done
