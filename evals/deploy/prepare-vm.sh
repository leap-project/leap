#!/bin/bash -x

bash install-lamp.sh
bash install-leap.sh
bash install-redcap.sh

unzip ham10000.zip
rm ham10000.zip

bash create-project.sh
