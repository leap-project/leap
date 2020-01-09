#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
openssl genrsa -out sitealgo.key 2048

# Create a signing request
openssl req -new -sha256 -key sitealgo.key -out sitealgo.csr

# Generate a signed certificate by passing the signing request and the CA key and certificate
openssl x509 -req -in sitealgo.csr -CA ../../certs/myCA.crt -CAkey ../../certs/myCA.key -CAcreateserial -out sitealgo.crt -days 365 -sha256