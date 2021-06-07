#!/bin/bash -x

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 3):"
    echo "[r-group, location]"
    exit
fi

rgroup=$1    # resource group in which to find the image/create VM
location=$2  # location to deploy network security group (e.g. westus)

sec_group_name="permissive-all-in-all-out-${location}"

az network nsg create -g $rgroup -n ${sec_group_name} --location $location --tags all_in all_out
az network nsg rule create -g $rgroup --nsg-name ${sec_group_name}  -n all_out --priority 100 \
   --source-address-prefixes '*' --source-port-ranges '*' \
   --destination-address-prefixes '*' --destination-port-ranges '*' \
   --direction Outbound --access Allow
az network nsg rule create -g $rgroup --nsg-name ${sec_group_name} -n all_in --priority 100 \
   --source-address-prefixes '*' --source-port-ranges '*' \
   --destination-address-prefixes '*' --destination-port-ranges '*' \
   --direction Inbound --access Allow
