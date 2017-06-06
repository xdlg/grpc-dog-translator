#!/bin/bash

python -m grpc.tools.protoc -I=protos/ --python_out=src --grpc_python_out=src protos/translator.proto

