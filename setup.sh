# Install protoc compiler and runtime
sudo apt-get install autoconf automake libtool curl make g++ unzip
cd
git clone https://github.com/protocolbuffers/protobuf.git
cd protobuf
git submodule update --init --recursive
./autogen.sh
./configure
make
make check
sudo make install
sudo ldconfig # refresh shared library cache
Get Go protocol buffer plugin

# Install protobuf for Go
go get -u github.com/golang/protobuf/protoc-gen-go
# Install protobuf for Python
pip install protobuf
# Install grpc for Go
go get -u google.golang.org/grpc
