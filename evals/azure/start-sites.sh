echo "Starting sites..."
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters (expecting 1):"
    echo "[num_sites]"
    exit
fi

n_sites=$1

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

for i in {1..15}
do
    echo "Starting site.${i}:"
    get_resource_group_name $i
    bash start-vm.sh $resource_group site.${i}

    if [ $i -eq $n_sites ]; then
      break
    fi
done
