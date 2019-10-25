#!/bin/bash

# Generate private key for certificate authority
openssl genrsa -des3 -out myCA.key 2048
# Generate root certificate
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem
# Next step is to install the .pem certificate just created to this device.