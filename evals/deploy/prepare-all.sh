#!/bin/bash -x
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir, user]"
    exit
fi

leap_dir=$1
user=$2

bash ${leap_dir}/evals/deploy/prepare-client.sh ${leap_dir} $user &
bash ${leap_dir}/evals/deploy/prepare-cloud.sh ${leap_dir} $user &
bash ${leap_dir}/evals/deploy/prepare-sites.sh ${leap_dir} $user &

for job in `jobs -p`
do
echo $job
wait $job
done