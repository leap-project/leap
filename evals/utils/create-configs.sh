#!/bin/bash -x

# Create config for cloud
python create-cloud-config.py

# Create config for sites
python create-site-config.py