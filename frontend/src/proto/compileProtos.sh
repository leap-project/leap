#!/bin/bash

# Compile computation-msgs.proto
protoc -I=. --js_out=import_style=commonjs:. computation-msgs.proto

# Compile cloud-algos.proto
protoc -I=. --js_out=import_style=commonjs:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:. cloud-algos.proto
