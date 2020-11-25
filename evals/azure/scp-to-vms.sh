#!/bin/bash -x


# Note: depends on sshpass to pass password to scp:
# https://gist.github.com/arunoda/7790979

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[local-filename]"
    exit
fi

filetoscp=$1    # local file to scp

./scp-to-vm.sh leap 13.71.186.132 $filetoscp
./scp-to-vm.sh leap 40.85.213.16 $filetoscp
./scp-to-vm.sh leap 40.85.210.139 $filetoscp
./scp-to-vm.sh leap 40.85.206.37 $filetoscp
./scp-to-vm.sh leap 40.85.205.66 $filetoscp
./scp-to-vm.sh leap 40.85.211.171 $filetoscp
./scp-to-vm.sh leap 40.85.208.112 $filetoscp
./scp-to-vm.sh leap 40.85.211.247 $filetoscp
./scp-to-vm.sh leap 40.85.214.151 $filetoscp
./scp-to-vm.sh leap 40.85.223.40 $filetoscp
./scp-to-vm.sh leap 40.85.209.157 $filetoscp
./scp-to-vm.sh leap 40.85.212.12 $filetoscp
./scp-to-vm.sh leap 40.85.210.241 $filetoscp
./scp-to-vm.sh leap 13.71.186.197 $filetoscp
./scp-to-vm.sh leap 40.85.212.140 $filetoscp
./scp-to-vm.sh leap 13.71.189.114 $filetoscp
./scp-to-vm.sh leap 40.85.208.226 $filetoscp
./scp-to-vm.sh leap 40.85.211.53 $filetoscp
./scp-to-vm.sh leap 40.85.215.103 $filetoscp
./scp-to-vm.sh leap 40.85.210.191 $filetoscp
./scp-to-vm.sh leap 40.85.213.85 $filetoscp
./scp-to-vm.sh leap 40.85.252.48 $filetoscp
./scp-to-vm.sh leap 40.85.214.201 $filetoscp

