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
# Install grpc for Python
# - Need pip to be version 9 or higher. Careful when updating
#   your pip version not to update your system pip. I recommend
#   using a virtual environment. To do this download virtual env
#   by issuing 'pip install virtualenv'. Then cd into your project
#   folder and run 'virtualenv venv'. This will create a folder
#   in the current dir containing the python executable files and
#   a copy of the pip library. Run 'source venv/bin/activate' to
#   begin using the virual environment. Install the grpc packages
#   using pip, and then run the 'deactivate' command in the ter-
#   minal.
pip install grpcio
pip install grpcio-tools
