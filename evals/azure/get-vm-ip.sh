#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[r-group, vm-name]"
    exit
fi

rgroup=$1   # resource group
vm=$2       # VM name whose IPs to retrieve

# This call fails for some reason:
# az vm list-ip-addresses -g $rgroup -n $vm -o table

# Hack:
az vm show --resource-group $rgroup --name $vm --show-details | grep -E 'publicIps|privateIps'