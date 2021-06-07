if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[path_ip_dir]"
    exit
fi

leap_dir=$1
path_ip_dir=${leap_dir}/evals/ips

resource_group="leap_westus"

get_resource_group_name() {
  case $((($1 - 1) % 5)) in
    0)
      resource_group=leap_westus
      ;;
    1)
      resource_group=leap_eastus
      ;;
    2)
      resource_group=leap_westeurope
      ;;
    3)
      resource_group=leap_eastasia
      ;;
    4)
      resource_group=leap_australiaeast
      ;;
    esac
}

echo "sites"
for i in {1..15}
do
    echo "site.${i}:"
#    get_resource_group_name $i
    result=$(bash ${leap_dir}/evals/azure/get-vm-ip.sh $resource_group site.${i})
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
result=$(bash ${leap_dir}/evals/azure/get-vm-ip.sh leap_westus client)
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
result=$(bash ${leap_dir}/evals/azure/get-vm-ip.sh leap_westus cloud)
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
