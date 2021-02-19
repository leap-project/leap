if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters (expecting 5):"
    echo "[n_sites, site_ip_path, cloud_ip_path, client_ip_path, filename]"
    exit
fi

n=$1
site_ip_path=$2
cloud_ip_path=$3
client_ip_path=$4
filename=$5

text=$(cat $filename)
command="${text} >> ~/.bashrc"

leap_dir="/home/stolet/Documents/MSC/leap/evals/utils"

i=0
for ip in $(cat $cloud_ip_path);do
    ssh stolet@$ip $command
done

i=0
for ip in $(cat client_ip_path);do
    ssh stolet@$ip $command
done

i=0
for ip in $(cat $site_ip_path);do
    ssh stolet@$ip $command
    i=$((i + 1))
    if [[ n -eq i ]]; then
        break
    fi
done