#!/bin/bash -x

echo "Stopping Sites..."
for i in {1..15}
do
    echo "Stopping site.${i}:"
    bash stop-vm.sh Leap site.${i}
done

