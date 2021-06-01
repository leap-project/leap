#!/bin/bash -x

user=stolet
leap_dir=/home/stolet/Documents/MSC/leap

# Create network security group in each region
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_westus" "westus"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_eastus" "eastus"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_westeurope" "westeurope"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_eastasia" "eastasia"
bash ${leap_dir}/evals/azure/create-nsg.sh "leap_australiaeast" "australiaeast"

## Deploy VMs in each region
#bash ${leap_dir}/evals/azure/create-all.sh $leap_dir
#
## Get ips
#bash ${leap_dir}/evals/azure/get-vms-ips.sh ${leap_dir}
#
## For each VM prepare the environment
#bash ${leap_dir}/evals/deploy/prepare-client.sh ${leap_dir} &
#bash ${leap_dir}/evals/deploy/prepare-cloud.sh ${leap_dir} &
#bash ${leap_dir}/evals/deploy/prepare-sites.sh ${leap_dir}
#
## Create ssl certs
#bash ${leap_dir}/evals/utils/create-all-certificates.sh 15
#
## Create configs
#bash ${leap_dir}/evals/utils/create-configs
#
#git add ${leap_dir}/.
#git commit -m "Updating configs and certificates"
#git push
#
#bash ${leap_dir}/evals/utils/pull-all.sh ${leap_dir}/ips-sites ${leap_dir}/ips-client ${leap_dir}/ips-cloud $user master