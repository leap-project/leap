#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
openssl genrsa -out cloudalgo.key 2048

# Create a signing request
openssl req -new -sha256 -key cloudalgo.key -out cloudalgo.csr

# Generate a signed certificate by passing the signing request and the CA key and certificate
openssl x509 -req -in cloudalgo.csr -CA ../../certs/myCA.crt -CAkey ../../certs/myCA.key -CAcreateserial -out cloudalgo.crt -days 365 -sha256