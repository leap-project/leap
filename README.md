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
go get -u github.com/golang/protobuf/protoc-gen-go
go get -u google.golang.org/grpc
go get -u github.com/sirupsen/logrus
go get -u github.com/rifflock/lfshook
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
The leap infrastructure is composed of 4 different programs: the site-algo, the site-connector, the coordinator, and the cloud-algo. Once these 4 programs are up and running, you can use the Leap API to perform some computations.

### Starting the Coordinator
The coordinator is what holds the system together. Tt talks to the site-connector and the cloud-algo. To start the coordinator go to the Exe directory and run the following command:
```
go run coordinator-main.go -ip=127.0.0.1:5000
```
`ip`: Ip and port of the coordinator  

### Starting the Site Connector
The site connector is the point of contact between each hospital site and the coordinator. To run the site connector go to the Exe directory and execute the following command: 
```
go run connector-main.go -ip=127.0.0.1:50001 -cip="127.0.0.1:50001" -aip="127.0.0.1:60000" -id=0
```
`id`: Id of this site  
`ip`: Ip and port of this site connector  
`cip`: Ip and port of the coordinator  
`aip`: The ip and port of the site algo in the same site  

### Starting the Site Algo
The site algo has access to a dataset and runs computations relayed to it. It responds to requests from the site-connector, which passes the results from the site-algo to the coordinator. Inside the SiteAlgo directory, type the following command:
```
python -m site_algo -ip=127.0.0.1:60000 -cip=127.0.0.1:50001
```
`ìp`: Ip and port of this site algo  
`cip`: Ip and port of the site connector in the same site  

### Starting the Cloud Algo
The cloud algo receives the results from all the sites through the coordinator. It then performs some computation using these results. To run the cloud algo, navigate to the CloudAlgo directory and enter the following command: 
```
python -m cloud_algo -ip=127.0.0.1:70000 -cip=127.0.0.1:50000
```
`ip`: The ip and port of the cloud algo  
`cip`: The ip and port of the coordinator

