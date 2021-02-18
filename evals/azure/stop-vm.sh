#!/bin/bash -x

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[r-group, vm-name]"
    exit
fi

rgroup=$1   # resource group
vm=$2       # VM name to stop

#echo 'Queueing up vm STOP with no-wait..'
#az vm stop --resource-group $rgroup --name $vm --no-wait

echo "Deallocating vm $vm"
az vm deallocate --resource-group $rgroup --name $vm --no-wait
