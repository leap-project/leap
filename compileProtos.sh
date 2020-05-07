#!/bin/bash

# Compile computation-msgs.proto
protoc -I=.  --go_out=proto/  proto/computation-msgs.proto
protoc -I=.  --python_out=.  proto/computation-msgs.proto

# Compile registration-msgs.proto
protoc -I=.  --go_out=proto/  proto/registration-msgs.proto
protoc -I=.  --python_out=.  proto/registration-msgs.proto

# Compile availability-msgs.proto
protoc -I=.  --go_out=proto/  proto/availability-msgs.proto
protoc -I=.  --python_out=.  proto/availability-msgs.proto

# Compile coordinator.proto
protoc -I=. --go_out=plugins=grpc:proto/ proto/coordinator.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. proto/coordinator.proto

# Compile cloud-algos.proto
protoc -I=. --go_out=plugins=grpc:proto/ proto/cloud-algos.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. proto/cloud-algos.proto

# Compile site-algos.proto
protoc -I=. --go_out=plugins=grpc:proto/ proto/site-algos.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. proto/site-algos.proto

# Compile site-connector.proto
protoc -I=. --go_out=plugins=grpc:proto/ proto/site-connector.proto
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. proto/site-connector.proto