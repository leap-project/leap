#!/bin/bash -x

bash create-vm.sh leap_westus client 'westus' &

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
