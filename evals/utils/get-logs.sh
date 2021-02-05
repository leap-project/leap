#!/bin/bash -x

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters (expecting 4):"
    echo "[n_sites, site_ip_path, cloud_ip_path]"
    exit
fi

n=$1
site_ip_path=$2
cloud_ip_path=$3
log_dir=$4

i=0
for ip in $(cat $site_ip_path);do
    scp stolet@$ip:/home/stolet/gopath/src/leap/exe/logs/site0.log $log_dir 
    scp stolet@$ip:/home/stolet/gopath/src/leap/exe/logs/sitealgo0.log $log_dir 
    
    i=$((i + 1))
    if [[ n -eq i ]]; then
        break
    fi
done

i=0
for ip in $(cat $cloud_ip_path);do
    scp stolet@$ip:/home/stolet/gopath/src/leap/exe/logs/coordinator.log $log_dir 
    scp stolet@$ip:/home/stolet/gopath/src/leap/exe/logs/cloudalgo.log $log_dir 
done

