#!/bin/bash -x

echo "Stopping VMs..."
for i in {1..22}
do
    echo "Stopping vm.${i}:"
    ./stop-vm.sh leap vm.${i}
done

