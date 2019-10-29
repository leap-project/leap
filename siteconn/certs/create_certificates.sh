#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
sudo openssl genrsa -out siteconn.key 2048

# Create a signing request
sudo openssl req -new -sha256 -key siteconn.key -out siteconn.csr

# Generate a signed certificate
sudo openssl x509 -req -in siteconn.csr -CA ../../certs/myCA.crt -CAkey ../../certs/myCA.key -CAcreateserial -out siteconn.crt -days 365 -sha256
sudo rm .srl