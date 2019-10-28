#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
sudo openssl genrsa -out coord.key 2048
# Generate certificate. This is a self-signed X.509 public key for distribution
sudo openssl req -new -x509 -sha256 -key coord.key -out coord.crt -days 3650
# Generate a certificate signing request to access the certificate authority
sudo openssl req -new -sha256 -key coord.key -out coord.csr
sudo openssl x509 -req -sha256 -in coord.csr -signkey coord.key -out coord.crt -days 3650
