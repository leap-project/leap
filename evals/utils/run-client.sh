#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters (expecting 2):"
    echo "[hostname, num_sites, command_type]"
    exit
fi

hostname=$1
n=$2
command_type=$3
leap_dir='/home/stolet/gopath/src/leap/api'
python_path='/home/stolet/anaconda3/envs/leap/bin/python'

echo "Running resnet"
command=""

if [[ $command_type == "resnet" ]]
then
  command="export GODEBUG=x509ignoreCN=0 && cd $leap_dir && $python_path -m resnet_example $n"
elif [[ $command_type == "logreg" ]]
then
  command="export GODEBUG=x509ignoreCN=0 && cd $leap_dir && $python_path -m logreg_example $n"
fi

ssh stolet@$hostname $command