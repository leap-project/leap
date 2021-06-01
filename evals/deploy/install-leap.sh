#!/bin/bash

# INSTALL GO
wget "https://golang.org/dl/go1.15.7.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.15.7.linux-amd64.tar.gz
echo | sudo tee -a ~/.bashrc
echo 'export PATH=$PATH:/usr/local/go/bin' | sudo tee -a ~/.bashrc 
echo | sudo tee -a ~/.bashrc
mkdir gopath
mkdir gopath/bin gopath/pkg gopath/src
echo 'export GOPATH=$HOME/gopath' | sudo tee -a ~/.bashrc
echo | sudo tee -a ~/.bashrc

source ~/.bashrc
go version

# INSTALL PYTHON
wget "https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh"
bash ~/Anaconda3-2021.05-Linux-x86_64.sh -b
~/anaconda3/bin/conda init bash
source ~/.bashrc
conda create -y --name leap python=3.7.9
echo | sudo tee -a ~/.bashrc
echo "conda activate leap" | sudo tee -a ~/.bashrc
echo | sudo tee -a ~/.bashrc
source ~/.bashrc

# INSTALL PROTOBUF

# Install tools to build protobuf
sudo apt-get install -y autoconf automake libtool curl make g++ unzip

# Clone protobuf repo
cd
git clone https://github.com/protocolbuffers/protobuf.git
cd protobuf
git submodule update --init --recursive
./autogen.sh

# Install protocol bugger runtime and compiler
./configure
make -j4
make check
sudo make install
sudo ldconfig
cd

echo | sudo tee -a ~/.bashrc
echo 'export PATH=$PATH:$GOPATH/bin' | sudo tee -a ~/.bashrc

# Clone LEAP and install necessary packages
cd gopath/src/
git clone https://github.com/leap-project/leap.git

pip install pandas==1.2.1
pip install protobuf==3.14.0
pip install grpcio==1.35.0
pip install grpcio-tools==1.35.0
pip install requests==2.25.1
pip install numpy==1.20.0
pip install pylogrus==0.4.0
pip install torch==1.7.1
pip install torchvision==0.8.2
pip install pillow==8.1.0
pip install ujson==4.0.2

go get -u github.com/golang/protobuf/protoc-gen-go
go get -u google.golang.org/grpc
go get -u github.com/sirupsen/logrus
go get -u github.com/rifflock/lfshook
go get -u golang.org/x/crypto/bcrypt
go get -u github.com/dgrijalva/jwt-go

go get github.com/mattn/go-sqlite3
go install github.com/mattn/go-sqlite3
export CGO_ENABLED=1

