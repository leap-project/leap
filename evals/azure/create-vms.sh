#!/bin/bash -x
# TODO: Change name of each VM
# for i in {1..11}
# do
#     ./create-vm.sh t p${i} proj1full t1 getreadytoBl0ckDra@wP
# done

./create-vm.sh leap vm.1 leap.image &
./create-vm.sh leap vm.2 leap.image &
./create-vm.sh leap vm.3 leap.image &
./create-vm.sh leap vm.4 leap.image &
./create-vm.sh leap vm.5 leap.image &
./create-vm.sh leap vm.6 leap.image &
./create-vm.sh leap vm.7 leap.image &
./create-vm.sh leap vm.8 leap.image &
./create-vm.sh leap vm.9 leap.image &
./create-vm.sh leap vm.10 leap.image &
./create-vm.sh leap vm.11 leap.image &
./create-vm.sh leap vm.12 leap.image &
./create-vm.sh leap vm.13 leap.image &
./create-vm.sh leap vm.14 leap.image &
./create-vm.sh leap vm.15 leap.image &
./create-vm.sh leap vm.16 leap.image &
./create-vm.sh leap vm.17 leap.image &
./create-vm.sh leap vm.18 leap.image &
./create-vm.sh leap vm.19 leap.image &
./create-vm.sh leap vm.20 leap.image &
./create-vm.sh leap vm.21 leap.image &
./create-vm.sh leap vm.22 leap.image &

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
