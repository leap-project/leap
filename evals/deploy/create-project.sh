#!/bin/bash

python create-project.py
token=$(cat token)
echo $token
cp token gopath/src/leap/config/token
