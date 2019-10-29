#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
sudo openssl genrsa -out cloudalgo.key 2048

# Create a signing request
sudo openssl req -new -sha256 -key cloudalgo.key -out cloudalgo.csr

# Generate a signed certificate
sudo openssl x509 -req -in cloudalgo.csr -CA ../../certs/myCA.crt -CAkey ../../certs/myCA.key -CAcreateserial -out cloudalgo.crt -days 365 -sha256
sudo rm .srl