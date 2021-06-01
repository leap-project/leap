#!/bin/bash -x
# for i in {1..11}
# do
#     ./create-vm.sh t p${i} proj1full t1 getreadytoBl0ckDra@wP
# done

bash create-vm.sh leap_westus site.1 'westus'&
bash create-vm.sh leap_eastus site.2 'eastus' &
bash create-vm.sh leap_westeurope site.3 'westeurope' &
bash create-vm.sh leap_eastasia site.4 'eastasia' &
bash create-vm.sh leap_australiaeast site.5 'australiaeast' &
bash create-vm.sh leap_westus site.6 'westus' &
bash create-vm.sh leap_eastus site.7 'eastus' &
bash create-vm.sh leap_westeurope site.8 'westeurope' &
bash create-vm.sh leap_eastasia site.9 'eastasia' &
bash create-vm.sh leap_australiaeast site.10 'australiaeast' &
bash create-vm.sh leap_westus site.11 'westus' &
bash create-vm.sh leap_eastus site.12 'eastus' &
bash create-vm.sh leap_westeurope site.13 'westeurope' &
bash create-vm.sh leap_eastasia site.14 'eastasia' &
bash create-vm.sh leap_australiaeast site.15 'australiaeast' &

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
