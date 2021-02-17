#!/bin/bash

leap_dir="/home/stolet/Documents/MSC/leap/evals"

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[num_sites]"
    exit
fi

n=$1

bash $leap_dir/utils/run-leap.sh $n $leap_dir/ips/site-ips.txt $leap_dir/ips/cloud-ip.txt $leap_dir/ips/client-ip.txt

#bash $leap_dir/utils/get-logs.sh 1 $leap_dir/ips/site-ips.txt $leap_dir/ips/cloud-ip.txt $leap_dir/performance-breakdown/logs
