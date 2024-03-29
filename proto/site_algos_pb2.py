# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/site-algos.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import computation_msgs_pb2 as proto_dot_computation__msgs__pb2
from proto import availability_msgs_pb2 as proto_dot_availability__msgs__pb2
from proto import selector_verification_msgs_pb2 as proto_dot_selector__verification__msgs__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/site-algos.proto',
  package='proto',
  syntax='proto3',
  serialized_options=b'Z\007.;proto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16proto/site-algos.proto\x12\x05proto\x1a\x1cproto/computation-msgs.proto\x1a\x1dproto/availability-msgs.proto\x1a&proto/selector-verification-msgs.proto2\xe1\x01\n\x08SiteAlgo\x12<\n\x03Map\x12\x16.proto.MapRequestChunk\x1a\x17.proto.MapResponseChunk\"\x00(\x01\x30\x01\x12\x43\n\rSiteAvailable\x12\x17.proto.SiteAvailableReq\x1a\x17.proto.SiteAvailableRes\"\x00\x12R\n\x0eVerifySelector\x12\x1e.proto.SelectorVerificationReq\x1a\x1e.proto.SelectorVerificationRes\"\x00\x42\tZ\x07.;protob\x06proto3'
  ,
  dependencies=[proto_dot_computation__msgs__pb2.DESCRIPTOR,proto_dot_availability__msgs__pb2.DESCRIPTOR,proto_dot_selector__verification__msgs__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_SITEALGO = _descriptor.ServiceDescriptor(
  name='SiteAlgo',
  full_name='proto.SiteAlgo',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=135,
  serialized_end=360,
  methods=[
  _descriptor.MethodDescriptor(
    name='Map',
    full_name='proto.SiteAlgo.Map',
    index=0,
    containing_service=None,
    input_type=proto_dot_computation__msgs__pb2._MAPREQUESTCHUNK,
    output_type=proto_dot_computation__msgs__pb2._MAPRESPONSECHUNK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SiteAvailable',
    full_name='proto.SiteAlgo.SiteAvailable',
    index=1,
    containing_service=None,
    input_type=proto_dot_availability__msgs__pb2._SITEAVAILABLEREQ,
    output_type=proto_dot_availability__msgs__pb2._SITEAVAILABLERES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='VerifySelector',
    full_name='proto.SiteAlgo.VerifySelector',
    index=2,
    containing_service=None,
    input_type=proto_dot_selector__verification__msgs__pb2._SELECTORVERIFICATIONREQ,
    output_type=proto_dot_selector__verification__msgs__pb2._SELECTORVERIFICATIONRES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SITEALGO)

DESCRIPTOR.services_by_name['SiteAlgo'] = _SITEALGO

# @@protoc_insertion_point(module_scope)
