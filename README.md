# LEAP
Leap is a Large-scale federated and privacy preserving Evaluation & Analysis Platform. It allows researchers to answer questions about any distributed medical data, while supporting primitives that can guarantee patient privacy. There are three basic parts to Leap: the client, the cloud, and the hospital sites. The Leap client is a set of programs that expose the API and is the point of interaction between the user and the platform. The cloud composes the main part of the infrastructure and is responsible for aggregating the results from each hospital. The third component is the hospital site, which runs computations/analysis on the dataset owned by that site.

## Setup

Before getting Leap installed you need to have Python 3.7 and Golang 1.10 installed. A good guide on how to get Golang up and running can be found [here](https://golang.org/doc/code.html). For Python, you can use a distribution such as [Anaconda](https://www.anaconda.com/distribution/#download-section).

### Protoc compiler and runtime
First you need to install the protoc compiler and runtime. This is necessary to get protocol buffers to work. Protocol buffers are used to serialize and deserialize the data transmitted through Leap. The protoc compiler and runtime can be installed by executing the commands below in your terminal.

Install some tools to build protobuf from source:
```
sudo apt-get install autoconf automake libtool curl make g++ unzip
```

Now clone the protobuf repository into a directory of your choice. In this example, the home directory is used. We will also clone the submodules and generate the configure script.
```
cd
git clone https://github.com/protocolbuffers/protobuf.git 
cd protobuf
git submodule update --init --recursive
./autogen.sh
```

The final step is to install the protocol buffer runtime and compiler. This may take a few minutes. If the make check fails, you can still install, but some features of the library may not work.
```
./configure 
make
make check
sudo make install
sudo ldconfig # refresh shared library cache.
```

### Go packages
We need to install the packages used by our Go programs. To install the packages, run the following commands in your terminal:
```
go get -u github.com/golang/protobuf/protoc-gen-go # Installs protobuf
go get -u google.golang.org/grpc # Installs grpc
go get -u github.com/sirupsen/logrus # Installs logrus
go get -u github.com/rifflock/lfshook # Enables colour at terminal with multiwriter
```

### Python packages
We also need to install the necessary python packages. The packages to be installed are below:
```
pip install pandas 
pip install protobuf 
pip install grpcio 
pip install grpcio-tools
pip install requests
pip install -e git+https://github.com/sburns/PyCap.git#egg=PyCap
pip install numpy
pip install pylogrus
pip install torch
```

## Running LEAP
To run the coordinator go to the coordinator folder and type `go run *.go` in your terminal. You can change the ip and ports the coordinator will be listening to by modifying the config.json file in the coordinator folder.

To run the site connector go to the site-connector folder and type `go run *.go` in your terminal. You can change the ip and ports the site-coonector will be listening to by modifying the config.json file in the coordinator folder.

To run a simple count query go to the cloud-algos folder and run `python count.py`.
