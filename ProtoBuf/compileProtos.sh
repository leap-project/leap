#!/bin/bash

# Compile computation-msgs.proto
protoc -I=. --go_out=.  computation-msgs.proto
protoc -I=. --python_out=. computation-msgs.proto

# Compile registration-msgs.proto
protoc -I=. --go_out=. registration-msgs.proto
protoc -I=. --python_out=. registration-msgs.proto

# Compile coordinator.proto
protoc -I=. --go_out=plugins=grpc:.  coordinator.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. coordinator.proto


# Compile cloud-algos.proto
protoc -I=. --go_out=plugins=grpc:.  cloud-algos.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. cloud-algos.proto

# Compile cloud-connector.proto
protoc -I=. --go_out=plugins=grpc:.  cloud-connector.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. cloud-connector.proto

# Compile site-algos.proto
protoc -I=. --go_out=plugins=grpc:.  site-algos.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. site-algos.proto

# Compile site-connector.proto
protoc -I=. --go_out=plugins=grpc:.  site-connector.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. site-connector.proto