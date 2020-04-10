#!/bin/bash

# Generate private RSA key to sign and authenticate the public key
openssl genrsa -out siteconn.key 2048

# Create a signing request
openssl req -new -sha256 -key siteconn.key -out siteconn.csr

# Generate a signed certificate by passing the signing request and the CA key and certificate
openssl x509 -req -in siteconn.csr -CA ../../certs/myCA.crt -CAkey ../../certs/myCA.key -CAcreateserial -out siteconn.crt -days 365 -sha256