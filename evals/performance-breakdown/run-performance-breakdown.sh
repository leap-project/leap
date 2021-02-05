#!/bin/bash

leap_dir="/home/stolet/Documents/MSC/leap/evals"

bash $leap_dir/utils/run-leap.sh 1 $leap_dir/ips/site-ips.txt $leap_dir/ips/cloud-ip.txt

bash $leap_dir/utils/get-logs.sh 1 $leap_dir/ips/site-ips.txt $leap_dir/ips/cloud-ip.txt $leap_dir/performance-breakdown/logs
