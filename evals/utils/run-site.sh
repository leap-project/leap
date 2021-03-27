#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters (expecting 2):"
    echo "[hostname, site_id]"
    exit
fi

hostname=$1
site_id=$2
leap_dir='/home/stolet/gopath/src/leap/exe'
python_path='/home/stolet/anaconda3/envs/leap/bin/python'

echo "Starting site connector"
config_name="../config/conn${site_id}-config.json"
command="export GODEBUG=x509ignoreCN=0 && export GOPATH=/home/stolet/gopath && cd $leap_dir && nohup /usr/local/go/bin/go run connector-main.go -config=${config_name} </dev/null >/dev/null 2>&1 &"
ssh stolet@$hostname $command &

echo "Starting site algo"
config_name="../config/sitealgo${site_id}_config.json"
command="export GODEBUG=x509ignoreCN=0 && cd $leap_dir && nohup $python_path -m sitealgo_main -config=${config_name} </dev/null >/dev/null 2>&1 &"
ssh stolet@$hostname $command &
