#!/bin/bash -x

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 3):"
    echo "[r-group, location]"
    exit
fi

rgroup=$1    # resource group in which to find the image/create VM
location=$2  # location to deploy network security group (e.g. westus)

az group create --location $location --name $rgroup