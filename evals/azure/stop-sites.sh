#!/bin/bash -x

echo "Stopping Sites..."
for i in {1..20}
do
    echo "Stopping site.${i}:"
    ./stop-vm.sh Leap site.${i}
done

