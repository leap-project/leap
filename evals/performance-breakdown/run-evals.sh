#!/bin/bash

leap_dir="/home/stolet/Documents/MSC/leap/evals"

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[number_of_sites, site_increment_step, number_of_runs, model_type]"
    exit
fi

n_sites=$1
sites_increment=$2
n_runs=$3
model_type=$4

for i in $(seq 0 ${sites_increment} ${n_sites}); do
  for j in $(seq 1 1 ${n_runs}); do
    sites=$i

    if [ $i -eq 0 ]; then
      sites=1
    fi

    # Train resnet-18
    bash $leap_dir/performance-breakdown/train-model.sh $sites $model_type

    # Kill all running nodes
    bash $leap_dir/utils/kill-all.sh $sites

    log_dir=${leap_dir}/performance-breakdown/logs/sites${sites}/run${j}
    mkdir -p $log_dir

    # Get logs from every site
    bash $leap_dir/utils/get-logs.sh $sites $leap_dir/ips/site-ips $leap_dir/ips/cloud-ips $leap_dir/ips/client-ips $log_dir
  done
done