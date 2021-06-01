#!/bin/bash -x
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1

bash ${leap_dir}/evals/azure/create-sites.sh $leap_dir
bash ${leap_dir}/evals/azure/create-client.sh $leap_dir
bash ${leap_dir}/evals/azure/create-cloud.sh $leap_dir

# wait for all the above to complete

for job in `jobs -p`
do
echo $job
wait $job
done
