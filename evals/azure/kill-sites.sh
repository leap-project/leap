#!/bin/bash

for line in $(cat site-ips);do
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
	echo "killing" $hostname
	ssh stolet@$hostname 'pkill sitealgo_main connector-main'
       
