if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters (expecting 3):"
    echo "[n_sites, path_ip_dir, filename]"
    exit
fi

n=$1
path_ip_dir=$2
filename=$3

#text=$(cat $filename)
command="cat $filename >> /home/stolet/.bashrc"
leap_dir="/home/stolet/Documents/MSC/leap/evals/utils"

echo "Modifying cloud bashrc"
i=0
for ip in $(cat "${path_ip_dir}/cloud-ips");do
    scp $filename stolet@$ip:
    ssh stolet@$ip $command
done

echo "Modifying client bashrc"
i=0
for ip in $(cat "${path_ip_dir}/client-ips");do
    scp $filename stolet@$ip:
    ssh stolet@$ip $command
done

i=0
for ip in $(cat "${path_ip_dir}/site-ips");do
  echo "Modifying site ${i} bashrc"
    scp $filename stolet@$ip:
    ssh stolet@$ip $command
    i=$((i + 1))
    if [[ n -eq i ]]; then
        break
    fi
done