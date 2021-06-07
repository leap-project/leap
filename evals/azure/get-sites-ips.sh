echo "IPs for sites:"

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

for i in {1..15}
do
#    get_resource_group_name $i
    echo "site.${i}:"
    ./get-vm-ip.sh $resource_group site.${i}
done

