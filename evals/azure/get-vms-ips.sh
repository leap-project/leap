if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[path_ip_dir]"
    exit
fi

path_ip_dir=$1

echo "IPs for testing machines:"
for i in {1..15}
do
    echo "site.${i}:"
    result=$(bash get-vm-ip.sh Leap site.${i})
    i=0
    for line in $result;do
        echo $line
        hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
        if [[ 1 -eq i ]]; then
            echo $hostname >> "${path_ip_dir}/site-private-ips"
        elif [[ 3 -eq i ]]; then
            echo $hostname >> "${path_ip_dir}/site-ips"
        fi
        i=$((i + 1))
    done
done

echo "client"
result=$(bash get-vm-ip.sh Leap client)
i=0
for line in $result;do
    hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
    if [[ 1 -eq i ]]; then
        echo $hostname >> "${path_ip_dir}/client-private-ips"
    elif [[ 3 -eq i ]]; then
        echo $hostname >> "${path_ip_dir}/client-ips"
    fi
    i=$((i + 1))
done

echo "cloud"
result=$(bash get-vm-ip.sh Leap cloud)
i=0
for line in $result;do
    hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`
    if [[ 1 -eq i ]]; then
        echo $hostname >> "${path_ip_dir}/cloud-private-ips"
    elif [[ 3 -eq i ]]; then
        echo $hostname >> "${path_ip_dir}/cloud-ips"
    fi
    i=$((i + 1))
done
