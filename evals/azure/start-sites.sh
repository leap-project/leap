echo "Starting sites..."
for i in {1..15}
do
    echo "Starting site.${i}:"
    ./start-vm.sh Leap site.${i}
done
