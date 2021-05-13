# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/cloud-algos.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import computation_msgs_pb2 as proto_dot_computation__msgs__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/cloud-algos.proto',
  package='proto',
  syntax='proto3',
  serialized_options=b'Z\007.;proto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17proto/cloud-algos.proto\x12\x05proto\x1a\x1cproto/computation-msgs.proto2G\n\tCloudAlgo\x12:\n\x07\x43ompute\x12\x15.proto.ComputeRequest\x1a\x16.proto.ComputeResponse\"\x00\x42\tZ\x07.;protob\x06proto3'
  ,
  dependencies=[proto_dot_computation__msgs__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_CLOUDALGO = _descriptor.ServiceDescriptor(
  name='CloudAlgo',
  full_name='proto.CloudAlgo',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=64,
  serialized_end=135,
  methods=[
  _descriptor.MethodDescriptor(
    name='Compute',
    full_name='proto.CloudAlgo.Compute',
    index=0,
    containing_service=None,
    input_type=proto_dot_computation__msgs__pb2._COMPUTEREQUEST,
    output_type=proto_dot_computation__msgs__pb2._COMPUTERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLOUDALGO)

DESCRIPTOR.services_by_name['CloudAlgo'] = _CLOUDALGO

# @@protoc_insertion_point(module_scope)