#!/bin/bash -x

user=stolet
leap_dir=/home/stolet/Documents/MSC/leap

# Create resource group in each region
bash ${leap_dir}/evals/azure/create-resource-group.sh "leap_westus" "westus"

# Create network security group in each region
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_westus" "westus"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_westus" "eastus"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_westus" "westeurope"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_westus" "eastasia"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_westus" "australiaeast"

# Deploy VMs in each region
bash ${leap_dir}/evals/azure/create-all.sh $leap_dir

# Create vnets that communicate with each other on each resource group
bash ${leap_dir}/evals/azure/create-vnets.sh "leap_westus"

## Get ips
bash ${leap_dir}/evals/azure/get-vms-ips.sh ${leap_dir}

# Start all VMs
bash ${leap_dir}/evals/azure/start-all.sh 15 $leap_dir
sleep 20

## For each VM prepare the environment
bash ${leap_dir}/evals/deploy/prepare-all.sh ${leap_dir} $user

# Create ssl certs
bash ${leap_dir}/evals/utils/create-all-certificates.sh 15

# Create configs
bash ${leap_dir}/evals/utils/create-configs

git add ${leap_dir}/.
git commit -m "Updating configs and certificates"
git push

bash ${leap_dir}/evals/utils/pull-all.sh ${leap_dir}/ips-sites ${leap_dir}/ips-client ${leap_dir}/ips-cloud $user master