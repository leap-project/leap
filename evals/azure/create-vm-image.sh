#!/bin/bash -x

# WARNING: you must have run this command BEFORE this script:
# sudo waagent -deprovision

echo 'WARNING: you must have run this command BEFORE this script:'
echo 'sudo waagent -deprovision'

read -r -p "Are you sure you want to proceed with image creation? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY])
        rgroup=$1    # resource group
        vm=$2        # vm name in the resource group
        imagename=$3 # imagename to create

        echo resource-group: $rgroup
        echo vm-name: $vm
        echo imagename: $imagename

        az vm deallocate --resource-group $rgroup --name $vm
        az vm generalize --resource-group $rgroup --name $vm
        az image create --resource-group $rgroup --source $vm --name $imagename

        ;;
    *)
        echo 'cancelled'
        ;;
esac
