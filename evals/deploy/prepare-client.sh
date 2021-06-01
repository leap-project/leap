#!/bin/bash -x

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[leap_dir]"
    exit
fi

leap_dir=$1

i=1
for line in $(cat ${leap_dir}/evals/ips/client-ips);do
	hostname=`echo $line | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'`

  scp prepare-vm.sh $(user)@$(hostname):
  scp install-lamp.sh $(user)@$(hostname):
  scp install-redcap.sh $(user)@$(hostname):
  scp install-leap.sh $(user)@$(hostname):
  scp redcap.sql $(user)@$(hostname):
  scp create-project.py $(user)@$(hostname):
  scp create-project.sh $(user)@$(hostname):
  scp ~/Desktop/ham10000.zip $(user)@$(hostname): # TODO: Don't hardcode this value

  ssh $(user)@$(ip) 'bash prepare-vm.sh'

  if [ $i -eq $n_sites ]; then
    break
  fi
  i=$((i + 1))
done