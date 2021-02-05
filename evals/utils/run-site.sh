#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters (expecting 1):"
    echo "[hostname]"
    exit
fi

hostname=$1
leap_dir='/home/stolet/gopath/src/leap/exe'
python_path='/home/stolet/anaconda3/envs/leap/bin/python'

echo "Starting site connector"
command="export GOPATH=/home/stolet/gopath && cd $leap_dir && /usr/local/go/bin/go run connector-main.go"
ssh stolet@$hostname $command &

echo "Starting site algo"
command="cd $leap_dir && $python_path -m sitealgo_main"
ssh stolet@$hostname $command & 
