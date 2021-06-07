echo "Starting sites..."
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters (expecting 1):"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1

echo "Starting cloud..."
bash ${leap_dir}/evals/azure/start-vm.sh leap_westus cloud