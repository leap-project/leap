#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
opensssl genrsa -out server.key 2048
# Generate certificate. This is a selg-signed X.509 public key for distribution
openssl req -new -x509 -sha256 -key server.key -out server.crt -days 3650
# Generate a certificate signing request to access the certificate authority
openssl req -new -sha256 -key server.key -out server.csr
openssl x509 -req -sha256 -in server.csr -signkey server.key -out server.crt -days 3650
