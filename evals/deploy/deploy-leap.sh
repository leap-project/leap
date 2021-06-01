#!/bin/bash -x

user=stolet
leap_dir=/home/stolet/Documents/MSC/leap

# Create network security group in each region
bash create-nsg.sh "leap_westus" "westus"
bash create-nsg.sh "leap_eastus" "eastus"
bash create-nsg.sh "leap_westeurope" "westeurope"
bash create-nsg.sh "leap_eastasia" "eastasia"
bash create-nsg.sh "leap_australiaeast" "australiaeast"

# Deploy VMs in each region
bash create-all.sh

# Get ips
bash get-vms-ips.sh ${leap_dir}/evals/ips

# For each VM prepare the environment

bash prepare-client.sh ${leap_dir} &
bash prepare-cloud.sh ${leap_dir} &
bash prepare-sites.sh ${leap_dir}

# Create ssl certs
bash create-all-certificates.sh 15

# Create configs
bash create-configs

git add ${leap_dir}/.
git commit -m "Updating configs and certificates"
git push

bash pull-all.sh ${leap_dir}/ips-sites ${leap_dir}/ips-client ${leap_dir}/ips-cloud $user master