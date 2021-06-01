#!/bin/bash -x

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

echo "Stopping Sites..."
for i in {1..15}
do
    echo "Stopping site.${i}:"
    get_resource_group_name $i
    bash stop-vm.sh Leap site.${i}
done

