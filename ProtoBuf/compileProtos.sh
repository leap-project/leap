#!/bin/bash

# Compile computation.proto
protoc -I=. --go_out=plugins=grpc:.  computation.proto
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. computation.proto

# Compile coordinator.proto
protoc -I=. --go_out=plugins=grpc:.  coordinator.proto
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. coordinator.proto

# Compile site-algos.proto
protoc -I=. --go_out=plugins=grpc:.  site-algos.proto
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. site-algos.proto

# Compile site-connector.proto
protoc -I=. --go_out=plugins=grpc:.  site-connector.proto
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. site-connector.proto