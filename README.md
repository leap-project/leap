# LEAP
Leap is a Large-scale federated and privacy preserving Evaluation & Analysis Platform. It allows researchers to answer questions about any distributed medical data, while supporting primitives that can guarantee patient privacy. There are three basic parts to Leap: the client, the cloud, and the hospital sites. The Leap client is a set of programs that expose the API and is the point of interaction between the user and the platform. The cloud composes the main part of the infrastructure and is responsible for aggregating the results from each hospital. The third component is the hospital site, which runs computations/analysis on the dataset owned by that site.

## Setup

Before getting Leap installed you need to have Python 3.7 and Golang 1.10 installed. A good guide on how to get Golang up and running can be found [here](https://golang.org/doc/code.html). For Python, you can use a distribution such as [Anaconda](https://www.anaconda.com/distribution/#download-section).

### Go Installation
```
wget "https://golang.org/dl/go1.15.7.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.15.7.linux-amd64.tar.gz
echo | sudo tee -a ~/.bashrc
echo 'export PATH=$PATH:/usr/local/go/bin' | sudo tee -a ~/.bashrc
echo | sudo tee -a ~/.bashrc
mkdir gopath
mkdir gopath/bin gopath/pkg gopath/src
echo 'export GOPATH=$HOME/gopath' | sudo tee -a ~/.bashrc
echo | sudo tee -a ~/.bashrc
echo 'export GODEBUG=x509ignoreCN=0' | sudo tee -a ~/.bashrc
source ~/.bashrc
go version
```
### Python Installation
wget "https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh"
bash ~/Anaconda3-2021.05-Linux-x86_64.sh -b
~/anaconda3/bin/conda init bash
source ~/.bashrc
conda create -y --name leap python=3.7.9
echo | sudo tee -a ~/.bashrc
echo "conda activate leap" | sudo tee -a ~/.bashrc
echo | sudo tee -a ~/.bashrc
source ~/.bashrc



#### Protoc compiler and runtime
First you need to install the protoc compiler and runtime. This is necessary to get protocol buffers to work. Protocol buffers are used to serialize and deserialize the data transmitted through Leap. The protoc compiler and runtime can be installed by executing the commands below in your terminal.

Install some tools to build protobuf from source:
```
sudo apt-get install -y autoconf automake libtool curl make g++ unzip
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
make -j4
make check
sudo make install
sudo ldconfig
cd

echo | sudo tee -a ~/.bashrc
echo 'export PATH=$PATH:$GOPATH/bin' | sudo tee -a ~/.bashrc
source ~/.bashrc
```
The compiler plugin for Go will be installed in `$GOPATH/bin`. Unless you have already set your `$GOBIN`, you must add `$GOPATH/bin` to your `$PATH` for the protocol compiler to find it. To do this, open `~/.bashrc` and add the following line to your .bashrc:
```
export PATH=$PATH:$GOPATH/bin
```

#### Cloning LEAP
The next step is to clone the LEAP repository in your computer. You can do this by navigating to your GOPATH and running `git clone https://github.com/bestchai/leap.git`in the terminal.

```
cd gopath/src/
git clone https://github.com/leap-project/leap.git
```

#### Python packages
We also need to install the necessary python packages. The packages to be installed are below:

```
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
```


#### Go packages
We need to install the packages used by our Go programs. To install the packages, run the following commands in your terminal:
```
go get -u github.com/golang/protobuf/protoc-gen-go
go get -u google.golang.org/grpc
go get -u github.com/sirupsen/logrus
go get -u github.com/rifflock/lfshook
go get -u golang.org/x/crypto/bcrypt
go get -u github.com/dgrijalva/jwt-go
```

### Installing MySQL
Make sure to have gcc installed in your machine because go-sqlite3 is a cgo package. Installing go-sqlite3 requires gcc, but after initial installation leap can run without relying on gcc.
```
go get github.com/mattn/go-sqlite3
go install github.com/mattn/go-sqlite3
export CGO_ENABLED=1
```

## Running LEAP
The leap infrastructure is composed of 4 different programs: the site-algo, the site-connector, the coordinator, and the cloud-algo. Once these 4 programs are up and running, you can use the Leap API to perform some computations.

Before starting the 4 different programs go to the main leap directory and run the following command to compile the proto files:
```
bash compileProtos.sh
```

#### Starting the Coordinator
The coordinator is what holds the system together. It talks to the site-connector and the cloud-algo. To start the coordinator go to the `exe` directory and run the following command:
```
go run coordinator-main.go -config=../config/coord-config.json
```
`config`: The path to the config file of the coordinator.  

#### Starting the Site Connector
The site connector is the point of contact between each hospital site and the coordinator. To run the site connector go to the `exe` directory and execute the following command: 
```
go run connector-main.go -config=../config/conn-config.json
```
`config`: The path to the config file of the site-connector.

#### Starting the Site Algo
The site algo has access to a dataset and runs computations relayed to it. It responds to requests from the site-connector, which passes the results from the site-algo to the coordinator. Inside the `exe` directory, type the following command:
```
python -m sitealgo_main -config=../config/sitealgo_config.json
```
`config`: The path to the config file of the site algo.  

#### Starting the Cloud Algo
The cloud algo receives the results from all the sites through the coordinator. It then performs some computation using these results. To run the cloud algo, navigate to the `exe` directory and enter the following command: 
```
python -m cloudalgo_main -config=../config/cloudalgo_config.json
```
`config`: The path to the config file of the cloud algo.

## Config Files
Each node in LEAP can be configured by using a json that gets passed as a parameter when the node gets initialized. Some of the things that can be configured using these config files are the ip and port of the node being configured, whether to use SSL/TLS to encrypt the connections, or the ID of the node.

#### Cloud Algo Config
`ip_port`: The ip and port the cloud algo is listening. Takes format of "ip:port" string.  
`coordinator_ip_port`: The ip and port the coordinator is listening. Takes format of "ip:port" string.  
`secure_with_tls`: Whether to use tls to secure connections between the cloud algo. Use "y" to enable TLS and "n" to disable it.  
`cert`: A string that gives the path to the location of the certificate for the cloud algo. Only used when TLS is enabled.  
`key`: A string that gives the path to the location of the private key for the cloud algo. Only used when TLS is enabled.   
`certificate_authority`: The path to the certificate from the certificate authority. Only used when TLS is enabled.  
`coord_cn`: The name given to the coordinator when its certificate is created. Only used when TLS is enabled.  

#### Coordinator Config
`IpPort`: The ip and port the coordinator is listening. Takes format of "ip:port" string.  
`Secure`: Whether to use tls to secure connections between the coordinator. Use true to enable TLS and false to disable it.  
`Crt`: A string that gives the path to the location of the certificate for the coordinator. Only used when TLS is enabled.  
`Key`: A string that gives the path to the location of the private key for the coordinator. Only used when TLS is enabled.   
`CertAuth`: The path to the certificate from the certificate authority. Only used when TLS is enabled.   
`SiteConnCN`: The name given to the site connector when its certificate is created. Only used when TLS is enabled.  

#### Site Connector Config
`IpPort`: The ip and port the site connector is listening. Takes format of "ip:port" string.  
`CoordinatorIpPort`: The ip and port the coordinator is listening. Takes format of "ip:port" string.  
`AlgoIpPort`: The ip and port the site algo is listening. Takes format of "ip:port" string.  
`SiteId`: The id of this side. An integer.  
`Secure`: Whether to use tls to secure connections between the site connector. Use true to enable TLS and false to disable it.  
`Crt`: A string that gives the path to the location of the certificate for the site connector. Only used when TLS is enabled.  
`Key`: A string that gives the path to the location of the private key for the site connector. Only used when TLS is enabled.   
`CertAuth`: The path to the certificate from the certificate authority. Only used when TLS is enabled.   
`CoordCN`: The name given to the coordinator when its certificate is created. Only used when TLS is enabled.  
`SiteAlgoCN`: The name given to the site algo when its certificate is created. Only used when TLS is enabled.  

#### Site Algo Config
`ip_port`: The ip and port the site algo is listening. Takes format of "ip:port" string.  
`connector_ip_port`: The ip and port the site connector is listening. Takes format of "ip:port" string.  
`csv_true`: Whether to grab data from a csv file.    
`secure_with_tls`: Whether to use tls to secure connections between the site algo. Use "y" to enable TLS and "n" to disable it.  
`cert`: A string that gives the path to the location of the certificate for the site algo. Only used when TLS is enabled.  
`key`: A string that gives the path to the location of the private key for the site algo. Only used when TLS is enabled.    
`certificate_authority`: The path to the certificate from the certificate authority. Only used when TLS is enabled.    

## Using Leap
Now that you have set up the infrastructure, you can start using Leap. Below we have a simple example on how to count the number of patients on each hospital site that are older than 50 and have a bmi of less than 25.
```python
import LeapApi.leap_fn as leap_fn
import LeapApi.leap as leap

predef_count = leap_fn.PredefinedFunction(algo_code=codes.COUNT_ALGO)

selector = "[age] > 50 and [bmi] < 25"
predef_count.selector = selector

dist_leap = leap.DistributedLeap(predef_count)
result = dist_leap.get_result()

```

You can also write your own algorithms. To create an algorithm, that counts the number of patients on each site you need to write the 8 abstract functions of Leap. For example:
```python
import pdb
import json
import inspect
import numpy as np

# Sum a particular column

def map_fns():

    def map_fn1(data, state):
        COUNT_SENSITIVITY = 1
        epsilon = privacy_params["epsilon"]
        delta = privacy_params["delta"]


        if delta == 0:
            noise = np.random.laplace(loc = 0, scale = COUNT_SENSITIVITY/float(epsilon), size = (1,1))
        else:
            sigma = (COUNT_SENSITIVITY/(epsilon))*np.sqrt(2*np.log(1.25/delta))
            noise = np.random.normal(0.0, sigma, 1)

        count = len(data) + noise.item()
        result = {
            "count": count
        }
        return json.dumps(result)

    return [map_fn1]

def agg_fns():

    def agg_fn1(map_results):
        s = 0
        for result in map_results:
            result = json.loads(result)
            s += result["count"]
        return s
    return [agg_fn1]

def update_fns():

    def update_fn1(agg_result, state):
        state["i"] += 1
        return state

    return [update_fn1]

# Returns which map/agg fn to run
def choice_fn(state):
    return 0

def dataprep_fn(data):
    return data

def stop_fn(agg_result, state):
    return state["i"] == 1

def postprocessing_fn(agg_result, state):
    return agg_result

def init_state_fn():
    state = {
        "i": 0,
    }
    return state
```

Now just send those functions over to Leap and get the result:
```python
udf_count = leap_fn.UDF()

selector = "[age] > 50 and [bmi] < 25"
udf_count.selector = selector
udf_count.map_fns = map_fns
udf_count.update_fns = update_fns
udf_count.agg_fns = agg_fns
udf_count.choice_fn = choice_fn
udf_count.stop_fn = stop_fn
udf_count.dataprep_fn = dataprep_fn
udf_count.postprocessing_fn = postprocessing_fn
udf_count.init_state_fn = init_state_fn

dist_leap = leap.DistributedLeap(udf_count)
result = dist_leap.get_result()
```
