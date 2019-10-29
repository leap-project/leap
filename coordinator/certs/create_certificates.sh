#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
sudo openssl genrsa -out coord.key 2048
# Generate certificate. This is a self-signed X.509 public key for distribution
#sudo openssl req -new -x509 -sha256 -key coord.key -out coord.crt -days 3650
# Generate a certificate signing request to access the certificate authority

# Create a signing request
sudo openssl req -new -sha256 -key coord.key -out coord.csr

# Generate a signed certificate
sudo openssl x509 -req -in coord.csr -CA ../../certs/myCA.crt -CAkey ../../certs/myCA.key -CAcreateserial -out coord.crt -days 365 -sha256
sudo rm .srl