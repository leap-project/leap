#!/bin/bash

leap_dir="/home/stolet/Documents/MSC/leap/evals"

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[num_sites]"
    exit
fi

n=$1

bash $leap_dir/utils/run-leap.sh $n $leap_dir/ips/site-ips $leap_dir/ips/cloud-ips $leap_dir/ips/client-ips

for ip in $(cat $leap_dir/ips/client-ips);do
  bash $leap_dir/utils/run-client.sh $ip $n
done
