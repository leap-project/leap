#!/bin/bash

leap_dir="/home/stolet/Documents/MSC/leap"

# Generate private key for certificate authority
openssl genrsa -out $leap_dir/certs/myCA.key 2048
# Generate root certificate
openssl req -x509 -new -nodes -key $leap_dir/certs/myCA.key -sha256 -days 1825 -out $leap_dir/certs/myCA.crt