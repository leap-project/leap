#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
sudo openssl genrsa -out sitealgo.key 2048
# Generate certificate. This is a selg-signed X.509 public key for distribution
sudo openssl req -new -x509 -sha256 -key sitealgo.key -out sitealgo.crt -days 3650
# Generate a certificate signing request to access the certificate authority
sudo openssl req -new -sha256 -key sitealgo.key -out sitealgo.csr
sudo openssl x509 -req -sha256 -in sitealgo.csr -signkey sitealgo.key -out sitealgo.crt -days 3650
