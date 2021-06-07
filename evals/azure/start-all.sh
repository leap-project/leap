if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 2):"
    echo "[num_sites, leap_dir]"
    exit
fi

n_sites=$1
leap_dir=$2

bash ${leap_dir}/evals/azure/start-client.sh $leap_dir
bash ${leap_dir}/evals/azure/start-sites.sh $n_sites $leap_dir
bash ${leap_dir}/evals/azure/start-cloud.sh $leap_dir