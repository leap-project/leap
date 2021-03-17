#!/bin/bash -x

if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters (expecting 5):"
    echo "[n_sites, site_ip_path, cloud_ip_path, client_ip_path, log_dir_path]"

    exit
fi

n=$1
site_ip_path=$2
cloud_ip_path=$3
client_ip_path=$4
log_dir=$5

i=0
for ip in $(cat $site_ip_path);do
    scp stolet@$ip:/home/stolet/gopath/src/leap/exe/logs/site${i}.log $log_dir
    scp stolet@$ip:/home/stolet/gopath/src/leap/exe/logs/sitealgo${i}.log $log_dir
    
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

i=0
for ip in $(cat $client_ip_path);do
    scp stolet@$ip:/home/stolet/gopath/src/leap/evals/baselines/logs/resnet_baseline.log $log_dir
done

