#!/bin/bash -x

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir, user]"
    exit
fi

leap_dir=$1
user=$2
deploy_dir=$leap_dir/evals/deploy

i=1
for line in $(cat ${leap_dir}/evals/ips/client-ips);do
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`

  scp -oStrictHostKeyChecking=no ${deploy_dir}/prepare-vm.sh $user@$hostname:
  scp -oStrictHostKeyChecking=no ${deploy_dir}/install-lamp.sh $user@$hostname:
  scp -oStrictHostKeyChecking=no ${deploy_dir}/install-redcap.sh $user@$hostname:
  scp -oStrictHostKeyChecking=no ${deploy_dir}/install-leap.sh $user@$hostname:
  scp -oStrictHostKeyChecking=no ${deploy_dir}/redcap.sql $user@$hostname:
  scp -oStrictHostKeyChecking=no ${deploy_dir}/create-project.py $user@$hostname:
  scp -oStrictHostKeyChecking=no ${deploy_dir}/create-project.sh $user@$hostname:
  scp -oStrictHostKeyChecking=no ~/Downloads/redcap11.0.5.zip $user@$hostname:
  scp -oStrictHostKeyChecking=no ~/Desktop/ham10000.zip $user@$hostname:

  # Delete line from bashrc that prevents ssh commands from executing using non interactive shell
  ssh ${user}@${hostname} "sed -i '/case \$- in/,+3d' ~/.bashrc"

  # Run script to prepare vm
  ssh ${user}@${hostname} "bash prepare-vm.sh"

  i=$((i + 1))
done