if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[path_ip_dir]"
    exit
fi

path_ip_dir=$1

resource_group=""

get_resource_group_name() {
  case $1 in
    (($1 == 0)) | (($1 == 5)) | (($1 == 10)))
      resource_group=leap_westus
      ;;
    (($1 == 1)) | (($1 == 6)) | (($1 == 11)))
      resource_group=east_us
      ;;
    (($1 == 2)) | (($1 == 7)) | (($1 == 12)))
      resource_group=west_europe
      ;;
    (($1 == 3)) | (($1 == 8)) | (($1 == 13)))
      resource_group=east_asia
      ;;
    (($1 == 4)) | (($1 == 9)) | (($1 == 14)))
      resource_group=australia_east
      ;;
  esac
}

echo "IPs for testing machines:"
for i in {1..15}
do
    echo "site.${i}:"
    get_resource_group_name $i
    result=$(bash get-vm-ip.sh $resource_group site.${i})
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
result=$(bash get-vm-ip.sh leap_westus client)
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
result=$(bash get-vm-ip.sh leap_westus cloud)
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
