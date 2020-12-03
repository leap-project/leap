echo "Starting sites..."
for i in {1..20}
do
    echo "Starting site.${i}:"
    ./start-vm.sh leap site.${i}
done
