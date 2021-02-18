#!/bin/bash -x
# for i in {1..11}
# do
#     ./create-vm.sh t p${i} proj1full t1 getreadytoBl0ckDra@wP
# done

bash create-vm.sh Leap cloud leap.image 'eastus' &

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
