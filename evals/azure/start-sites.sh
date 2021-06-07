echo "Starting sites..."
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 2):"
    echo "[num_sites, leap_dir]"
    exit
fi

n_sites=$1
leap_dir=$2

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
    echo "Starting site.${i}:"
#    get_resource_group_name $i
    bash ${leap_dir}/evals/azure/start-vm.sh $resource_group site.${i}

    if [ $i -eq $n_sites ]; then
      break
    fi
done
