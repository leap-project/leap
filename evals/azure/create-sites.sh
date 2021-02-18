#!/bin/bash -x
# for i in {1..11}
# do
#     ./create-vm.sh t p${i} proj1full t1 getreadytoBl0ckDra@wP
# done

bash create-vm.sh Leap site.1 leap.image 'eastus'&
bash create-vm.sh Leap site.2 leap.image 'westus' &
bash create-vm.sh Leap site.3 leap.image 'centralindia' &
bash create-vm.sh Leap site.4 leap.image 'japaneast' &
bash create-vm.sh Leap site.5 leap.image 'australiaeast' &
bash create-vm.sh Leap site.6 leap.image 'westeurope' &
bash create-vm.sh Leap site.7 leap.image 'eastus' &
bash create-vm.sh Leap site.8 leap.image 'westus' &
bash create-vm.sh Leap site.9 leap.image 'centralindia' &
bash create-vm.sh Leap site.10 leap.image 'japaneast' &
bash create-vm.sh Leap site.11 leap.image 'australiaeast' &
bash create-vm.sh Leap site.12 leap.image 'westeurope' &
bash create-vm.sh Leap site.13 leap.image 'eastus' &
bash create-vm.sh Leap site.14 leap.image 'westus' &
bash create-vm.sh Leap site.15 leap.image 'westeurope' &


# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
