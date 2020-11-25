echo "IPs for testing machines:"
for i in {1..22}
do
    echo "vm.${i}:"
    ./get-vm-ips.sh leap vm.${i}
done
