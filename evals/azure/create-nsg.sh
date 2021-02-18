#!/bin/bash -x

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 3):"
    echo "[r-group, location]"
    exit
fi

rgroup=$1    # resource group in which to find the image/create VM
location=$2  # location to deploy network security group (e.g. westus)

az network nsg create -g $rgroup -n permissive-all-in-all-out --location $location --tags all_in all_out