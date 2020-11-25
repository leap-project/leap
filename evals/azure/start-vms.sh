echo "Starting VMs..."
for i in {1..22}
do
    echo "Starting vm.${i}:"
    ./start-vm.sh leap vm.${i}
done

