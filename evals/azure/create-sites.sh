#!/bin/bash -x
# for i in {1..11}
# do
#     ./create-vm.sh t p${i} proj1full t1 getreadytoBl0ckDra@wP
# done

./create-vm.sh leap site.1 leap.image &
./create-vm.sh leap site.2 leap.image &
./create-vm.sh leap site.3 leap.image &
./create-vm.sh leap site.4 leap.image &
./create-vm.sh leap site.5 leap.image &
./create-vm.sh leap site.6 leap.image &
./create-vm.sh leap site.7 leap.image &
./create-vm.sh leap site.8 leap.image &
./create-vm.sh leap site.9 leap.image &
./create-vm.sh leap site.10 leap.image &
./create-vm.sh leap site.11 leap.image &
./create-vm.sh leap site.12 leap.image &
./create-vm.sh leap site.13 leap.image &
./create-vm.sh leap site.14 leap.image &
./create-vm.sh leap site.15 leap.image &
./create-vm.sh leap site.16 leap.image &
./create-vm.sh leap site.17 leap.image &
./create-vm.sh leap site.18 leap.image &
./create-vm.sh leap site.19 leap.image &
./create-vm.sh leap site.20 leap.image &

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
