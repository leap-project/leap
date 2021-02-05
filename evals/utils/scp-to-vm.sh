#!/bin/bash -x

# Note: depends on sshpass to pass password to scp:
# https://gist.github.com/arunoda/7790979

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[username, password, vmIP, local-filename]"
    exit
fi

username=$1     # username for scp
pws=$2          # password for scp
vmip=$3         # ip of the vm to scp to
filetoscp=$4    # local file to scp

scp -o "StrictHostKeyChecking no" $filetoscp ${username}@${vmip}:~/

# sshpass -p "${pws}" ssh -o "StrictHostKeyChecking no" ${username}@${vmip} '
# for i in `ls -d proj1_*`
# do
# echo $i
# cp ~/server.ip ~/${i}/
# cp ~/miners.ip ~/${i}/
# done
# '

