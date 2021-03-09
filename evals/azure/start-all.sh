if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters (expecting 1):"
    echo "[num_sites]"
    exit
fi

n_sites=$1

bash start-client.sh
bash start-sites.sh $n_sites
bash start-cloud.sh