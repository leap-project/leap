#!/bin/bash

# This script starts Leap with n sites. each with one algo
# Usage:   $ bash startLeap.sh n
# Example: $ bash starLeap.sh 3

# Number of sites to bring up
let n=$1

# Start coordinator
cd ~/gopath/src/leap/Coordinator/
go run *.go &
sleep 1s

# Start n site connectors with one algo on each site
connectorPortCount=2
algosPortCount=0

i=0
end=$((n - 1))
while [ $i -le $end ]
do
    # Start connector
    cd ~/gopath/src/leap/SiteConnector/

    listenCoordinatorPort=$((50000 + connectorPortCount))
    connectorPortCount=$((connectorPortCount + 1))
    listenAlgosPort=$((50000 + connectorPortCount))
    connectorPortCount=$((connectorPortCount + 1))
    go run *.go -cip="127.0.0.1:$listenCoordinatorPort" -aip="127.0.0.1:$listenAlgosPort" -id=$((i + 0)) &
    sleep 1s

    # Start site algo
    algoPort=$((60000 + $algosPortCount))
    algosPortCount=$((algosPortCount + 1))
    cd ~/gopath/src/leap/SiteAlgos/
    source ../venv/bin/activate
    python -m count -ip="127.0.0.1:$algoPort" -cip="127.0.0.1:$listenAlgosPort" &

    i=$((i + 1))
done
