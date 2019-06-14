#!/bin/bash

# WARNING: Don't spawn too many clients. Redcap at BC Children's
# has a limit of 100 requests per minute.

# This script starts n leap clients
# Usage:   $ bash spawnClients.sh n
# Example: $ bash starLeap.sh 3

let n=$1

source venv/bin/activate
cd CloudAlgos

i=0
end=$((n - 1))

while [ $i -le $end ]
do
    python -m count &
    i=$((i + 1))
done