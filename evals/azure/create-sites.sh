#!/bin/bash -x

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1

bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.1 'westus' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.2 'eastus' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.3 'westeurope' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.4 'eastasia' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.5 'australiaeast' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.6 'westus' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.7 'eastus' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.8 'westeurope' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.9 'eastasia' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.10 'australiaeast' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.11 'westus' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.12 'eastus' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.13 'westeurope' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.14 'eastasia' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&
bash ${leap_dir}/evals/azure/create-vm.sh leap_westus site.15 'australiaeast' "Canonical:UbuntuServer:18.04-LTS:18.04.202105120"&

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
