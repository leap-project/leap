#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 2):"
    echo "[hostname, num_sites]"
    exit
fi

hostname=$1
n=$2
leap_dir='/home/stolet/gopath/src/leap/api'
python_path='/home/stolet/anaconda3/envs/leap/bin/python'

echo "Running resnet"
command="export GODEBUG=x509ignoreCN=0 && cd $leap_dir && $python_path -m resnet_example $n"
ssh stolet@$hostname $command