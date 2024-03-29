#!/bin/bash -x
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1

bash $leap_dir/evals/azure/create-vm.sh leap_westus cloud 'westus' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120" &

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
