#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[num_sites]"
    exit
fi

num_sites=$1

leap_dir="/home/stolet/Documents/MSC/leap/evals"

bash $leap_dir/utils/kill-cloud.sh "${leap_dir}/ips/cloud-ips"
bash $leap_dir/utils/kill-sites.sh "${leap_dir}/ips/site-ips" $num_sites

