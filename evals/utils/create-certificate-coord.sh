#!/bin/bash

leap_dir="/home/stolet/Documents/MSC/leap"

# Generate private RSA key to sign and authenticate the public key
openssl genrsa -out $leap_dir/certs/coord.key 2048

# Create a signing request
openssl req -new -sha256 -key $leap_dir/certs/coord.key -out $leap_dir/certs/coord.csr

# Generate a signed certificate by passing the signing request and the CA key and certificate
openssl x509 -req -in $leap_dir/certs/coord.csr -CA $leap_dir/certs/myCA.crt -CAkey $leap_dir/certs/myCA.key -CAcreateserial -out $leap_dir/certs/coord.crt -days 365 -sha256