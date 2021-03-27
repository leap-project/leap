#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[sites_ip_file_path, cloud_ip_file_path, client_ip_file_path, num_sites]"
    exit
fi

filepath_sites=$1
filepath_cloud=$2
filepath_client=$3
n_sites=$4

echo "Kill bitnami in client"
for line in $(cat $filepath_client);do
  echo "killing" $hostname
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
	ssh stolet@$hostname 'sudo /opt/bitnami/ctlscript.sh stop'
done

echo "Kill bitnami in cloud"
for line in $(cat $filepath_cloud);do
  echo "killing" $hostname
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
	ssh stolet@$hostname 'sudo /opt/bitnami/ctlscript.sh stop'
done

echo "Kill bitnami in sites"
i=1
for line in $(cat $filepath_sites);do
  echo "killing" $hostname
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
	ssh stolet@$hostname 'sudo /opt/bitnami/ctlscript.sh stop'

  if [ $i -eq $n_sites ]; then
    break
  fi
  i=$((i + 1))
done
