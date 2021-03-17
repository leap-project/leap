#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "usage:"
    echo "[site_id]"
    exit
fi

leap_dir="/home/stolet/Documents/MSC/leap"

site_id=$1

# Generate private RSA key to sign and authenticate the public key
openssl genrsa -out $leap_dir/certs/sitealgo${site_id}.key 2048

# Create a signing request
openssl req -new -sha256 -key $leap_dir/certs/sitealgo${site_id}.key -out $leap_dir/certs/sitealgo${site_id}.csr

# Generate a signed certificate by passing the signing request and the CA key and certificate
openssl x509 -req -in $leap_dir/certs/sitealgo${site_id}.csr -CA $leap_dir/certs/myCA.crt -CAkey $leap_dir/certs/myCA.key -CAcreateserial -out $leap_dir/certs/sitealgo${site_id}.crt -days 365 -sha256