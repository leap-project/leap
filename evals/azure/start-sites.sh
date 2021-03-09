echo "Starting sites..."
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters (expecting 1):"
    echo "[num_sites]"
    exit
fi

n_sites=$1

for i in {1..15}
do
    echo "Starting site.${i}:"
    bash start-vm.sh Leap site.${i}

    if [ $i -eq $n_sites ]; then
      break
    fi
done
