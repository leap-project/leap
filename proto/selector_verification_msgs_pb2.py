# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/selector-verification-msgs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/selector-verification-msgs.proto',
  package='proto',
  syntax='proto3',
  serialized_options=b'Z\007.;proto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n&proto/selector-verification-msgs.proto\x12\x05proto\"U\n\x17SelectorVerificationReq\x12\x0e\n\x06siteId\x18\x01 \x01(\x03\x12\x10\n\x08selector\x18\x02 \x01(\t\x12\x18\n\x10isSelectorString\x18\x03 \x01(\x08\"I\n\x17SelectorVerificationRes\x12\x0e\n\x06siteId\x18\x01 \x01(\x03\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\r\n\x05\x65rror\x18\x03 \x01(\t\"F\n\x18SelectorVerificationsReq\x12\x10\n\x08selector\x18\x01 \x01(\t\x12\x18\n\x10isSelectorString\x18\x02 \x01(\x08\"M\n\x18SelectorVerificationsRes\x12\x31\n\tresponses\x18\x01 \x03(\x0b\x32\x1e.proto.SelectorVerificationResB\tZ\x07.;protob\x06proto3'
)




_SELECTORVERIFICATIONREQ = _descriptor.Descriptor(
  name='SelectorVerificationReq',
  full_name='proto.SelectorVerificationReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='siteId', full_name='proto.SelectorVerificationReq.siteId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='selector', full_name='proto.SelectorVerificationReq.selector', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isSelectorString', full_name='proto.SelectorVerificationReq.isSelectorString', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=134,
)


_SELECTORVERIFICATIONRES = _descriptor.Descriptor(
  name='SelectorVerificationRes',
  full_name='proto.SelectorVerificationRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='siteId', full_name='proto.SelectorVerificationRes.siteId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='success', full_name='proto.SelectorVerificationRes.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error', full_name='proto.SelectorVerificationRes.error', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=136,
  serialized_end=209,
)


_SELECTORVERIFICATIONSREQ = _descriptor.Descriptor(
  name='SelectorVerificationsReq',
  full_name='proto.SelectorVerificationsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='selector', full_name='proto.SelectorVerificationsReq.selector', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isSelectorString', full_name='proto.SelectorVerificationsReq.isSelectorString', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=211,
  serialized_end=281,
)


_SELECTORVERIFICATIONSRES = _descriptor.Descriptor(
  name='SelectorVerificationsRes',
  full_name='proto.SelectorVerificationsRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='responses', full_name='proto.SelectorVerificationsRes.responses', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=283,
  serialized_end=360,
)

_SELECTORVERIFICATIONSRES.fields_by_name['responses'].message_type = _SELECTORVERIFICATIONRES
DESCRIPTOR.message_types_by_name['SelectorVerificationReq'] = _SELECTORVERIFICATIONREQ
DESCRIPTOR.message_types_by_name['SelectorVerificationRes'] = _SELECTORVERIFICATIONRES
DESCRIPTOR.message_types_by_name['SelectorVerificationsReq'] = _SELECTORVERIFICATIONSREQ
DESCRIPTOR.message_types_by_name['SelectorVerificationsRes'] = _SELECTORVERIFICATIONSRES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SelectorVerificationReq = _reflection.GeneratedProtocolMessageType('SelectorVerificationReq', (_message.Message,), {
  'DESCRIPTOR' : _SELECTORVERIFICATIONREQ,
  '__module__' : 'proto.selector_verification_msgs_pb2'
  # @@protoc_insertion_point(class_scope:proto.SelectorVerificationReq)
  })
_sym_db.RegisterMessage(SelectorVerificationReq)

SelectorVerificationRes = _reflection.GeneratedProtocolMessageType('SelectorVerificationRes', (_message.Message,), {
  'DESCRIPTOR' : _SELECTORVERIFICATIONRES,
  '__module__' : 'proto.selector_verification_msgs_pb2'
  # @@protoc_insertion_point(class_scope:proto.SelectorVerificationRes)
  })
_sym_db.RegisterMessage(SelectorVerificationRes)

SelectorVerificationsReq = _reflection.GeneratedProtocolMessageType('SelectorVerificationsReq', (_message.Message,), {
  'DESCRIPTOR' : _SELECTORVERIFICATIONSREQ,
  '__module__' : 'proto.selector_verification_msgs_pb2'
  # @@protoc_insertion_point(class_scope:proto.SelectorVerificationsReq)
  })
_sym_db.RegisterMessage(SelectorVerificationsReq)

SelectorVerificationsRes = _reflection.GeneratedProtocolMessageType('SelectorVerificationsRes', (_message.Message,), {
  'DESCRIPTOR' : _SELECTORVERIFICATIONSRES,
  '__module__' : 'proto.selector_verification_msgs_pb2'
  # @@protoc_insertion_point(class_scope:proto.SelectorVerificationsRes)
  })
_sym_db.RegisterMessage(SelectorVerificationsRes)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
