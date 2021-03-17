
#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters (expecting):"
    echo "[n_sites, site_ip_path, cloud_ip_path]"
    exit
fi

n=$1
site_ip_path=$2
cloud_ip_path=$3

leap_dir="/home/stolet/Documents/MSC/leap/evals/utils"

i=0
for ip in $(cat $cloud_ip_path);do
    bash $leap_dir/run-cloud.sh $ip
done

sleep 8

i=0
for ip in $(cat $site_ip_path);do
    bash $leap_dir/run-site.sh $ip $i
    i=$((i + 1))
    if [[ n -eq i ]]; then
        break
    fi
done

sleep 2

#for ip in $(cat $client_ip_path);do
#  bash $leap_dir/run-client.sh $ip $n
#done



