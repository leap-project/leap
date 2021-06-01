#!/bin/bash -x

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1

bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.1 'westus'&
bash ${leap_dir}/evals/azure/create-vm.sh leap_eastus site.2 'eastus' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_westeurope site.3 'westeurope' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_eastasia site.4 'eastasia' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_australiaeast site.5 'australiaeast' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.6 'westus' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_eastus site.7 'eastus' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_westeurope site.8 'westeurope' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_eastasia site.9 'eastasia' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_australiaeast site.10 'australiaeast' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.11 'westus' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_eastus site.12 'eastus' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_westeurope site.13 'westeurope' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_eastasia site.14 'eastasia' &
bash ${leap_dir}/evals/azure/create-vm.sh leap_australiaeast site.15 'australiaeast' &

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
