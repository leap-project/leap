#!/bin/bash

for line in $(cat cloud-ip);do
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
	echo "killing" $hostname
	ssh stolet@$hostname 'pkill cloudalgo_main coordinator-main'
       
