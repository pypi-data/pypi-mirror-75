# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/api/operation.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/api/operation.proto',
  package='yandex.cloud.api',
  syntax='proto3',
  serialized_options=b'Z8github.com/yandex-cloud/go-genproto/yandex/cloud/api;api',
  serialized_pb=b'\n yandex/cloud/api/operation.proto\x12\x10yandex.cloud.api\x1a google/protobuf/descriptor.proto\"/\n\tOperation\x12\x10\n\x08metadata\x18\x01 \x01(\t\x12\x10\n\x08response\x18\x02 \x01(\t:P\n\toperation\x12\x1e.google.protobuf.MethodOptions\x18\xa6\xaa\x05 \x01(\x0b\x32\x1b.yandex.cloud.api.OperationB:Z8github.com/yandex-cloud/go-genproto/yandex/cloud/api;apib\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])


OPERATION_FIELD_NUMBER = 87334
operation = _descriptor.FieldDescriptor(
  name='operation', full_name='yandex.cloud.api.operation', index=0,
  number=87334, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)


_OPERATION = _descriptor.Descriptor(
  name='Operation',
  full_name='yandex.cloud.api.Operation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='yandex.cloud.api.Operation.metadata', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='yandex.cloud.api.Operation.response', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=88,
  serialized_end=135,
)

DESCRIPTOR.message_types_by_name['Operation'] = _OPERATION
DESCRIPTOR.extensions_by_name['operation'] = operation
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Operation = _reflection.GeneratedProtocolMessageType('Operation', (_message.Message,), {
  'DESCRIPTOR' : _OPERATION,
  '__module__' : 'yandex.cloud.api.operation_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.api.Operation)
  })
_sym_db.RegisterMessage(Operation)

operation.message_type = _OPERATION
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(operation)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
