#!/bin/bash -x

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 2):"
    echo "[leap_dir, resource_group]"
    exit
fi

leap_dir=$1
resource_group=$2

echo "Stopping Sites..."
for i in {1..15}
do
    echo "Stopping site.${i}:"
    bash ${leap_dir}/evals/azure/stop-vm.sh $resource_group site.${i}
done

