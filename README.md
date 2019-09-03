# LEAP
Leap project

Leap is a Large-scale federated and privacy preserving Evaluation & Analysis Platform. It allows researchers to answer questions about any distributed medical data, while supporting primitives that can guarantee patient privacy. There are three basic parts to Leap: the client, the cloud, and the hospital sites. The Leap client is a set of programs that expose the API and is the point of interaction between the user and the platform. The cloud composes the main part of the infrastructure and is responsible for aggregating the results from each hospital. The third component is the hospital site, which runs computations/analysis on the dataset owned by that site.

## Setup
1. Install Go


2. Install Python
3. Install protoc compiler and runtime
- `sudo apt-get install autoconf automake libtool curl make g++ unzip`
- `cd`
- `git clone https://github.com/protocolbuffers/protobuf.git`
- `cd protobuf`
- `git submodule update --init --recursive`
- `./autogen.sh`
- `./configure`
- `make`
- `make check`
- `sudo make install`
- `sudo ldconfig # refresh shared library cache`
- `Get Go protocol buffer plugin`
4. Install necessary Go packages
- `go get -u github.com/golang/protobuf/protoc-gen-go`
- `go get -u github.com/golang/protobuf/protoc-gen-go`
5. Install necessary Python packages
- `pip install protobuf`
- `pip install grpcio`
- `pip install grpcio-tools`

## Running LEAP
To run the coordinator go to the coordinator folder and type `go run *.go` in your terminal. You can change the ip and ports the coordinator will be listening to by modifying the config.json file in the coordinator folder.

To run the site connector go to the site-connector folder and type `go run *.go` in your terminal. You can change the ip and ports the site-coonector will be listening to by modifying the config.json file in the coordinator folder.

To run a simple count query go to the cloud-algos folder and run `python count.py`.
