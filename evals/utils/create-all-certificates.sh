#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[n_sites]"
    exit
fi

n_sites=$1

leap_dir="/home/stolet/Documents/MSC/leap"

mkdir -p $leap_dir/certs

cat "${leap_dir}/evals/utils/create-ca-input" | bash $leap_dir/evals/utils/create-ca.sh
echo "Created certificate authority"

cat "${leap_dir}/evals/utils/create-certificate-cloud-input" | bash $leap_dir/evals/utils/create-certificate-coord.sh
echo "Created certificates for coordinator"

cat "${leap_dir}/evals/utils/create-certificate-cloud-input" | bash $leap_dir/evals/utils/create-certificate-cloud.sh
echo "Created certificates for cloud algo"

for i in $(seq 0 1 $((n_sites-1))); do
  cat "${leap_dir}/evals/utils/create-certificate-sitealgo-input" | bash $leap_dir/evals/utils/create-certificate-sitealgo.sh $i
  cat "${leap_dir}/evals/utils/create-certificate-siteconn-input" | bash $leap_dir/evals/utils/create-certificate-siteconn.sh $i
  echo "Created certificates for site ${i}"
done