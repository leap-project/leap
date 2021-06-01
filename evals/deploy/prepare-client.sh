#!/bin/bash -x

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1
deploy_dir=$leap_dir/evals/deploy

i=1
for line in $(cat ${leap_dir}/evals/ips/client-ips);do
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`

  scp ${deploy_dir}/prepare-vm.sh $(user)@$(hostname):
  scp ${deploy_dir}/install-lamp.sh $(user)@$(hostname):
  scp ${deploy_dir}/install-redcap.sh $(user)@$(hostname):
  scp ${deploy_dir}/install-leap.sh $(user)@$(hostname):
  scp ${deploy_dir}/redcap.sql $(user)@$(hostname):
  scp ${deploy_dir}/create-project.py $(user)@$(hostname):
  scp ${deploy_dir}/create-project.sh $(user)@$(hostname):
  scp ~/Desktop/ham10000.zip $(user)@$(hostname):

  ssh $(user)@$(ip) 'bash prepare-vm.sh'

  if [ $i -eq $n_sites ]; then
    break
  fi
  i=$((i + 1))
done