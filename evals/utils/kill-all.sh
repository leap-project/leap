#!/bin/bash

leap_dir="/home/stolet/Documents/MSC/leap/evals"

bash $leap_dir/utils/kill-cloud.sh "${leap_dir}/ips/cloud-ip.txt"
bash $leap_dir/utils/kill-sites.sh "${leap_dir}/ips/site-ips.txt"

