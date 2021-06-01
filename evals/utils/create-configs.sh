#!/bin/bash -x

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1

# Create config for cloud
python ${leap_dir}/evals/utils/create-cloud-config.py

# Create config for sites
python ${leap_dir}/evals/utils/create-site-config.py