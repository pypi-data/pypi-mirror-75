# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/getInfoParam.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='qlua/rpc/getInfoParam.proto',
  package='qlua.rpc.getInfoParam',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\x1bqlua/rpc/getInfoParam.proto\x12\x15qlua.rpc.getInfoParam\"\x1a\n\x04\x41rgs\x12\x12\n\nparam_name\x18\x01 \x01(\t\"\x1c\n\x06Result\x12\x12\n\ninfo_param\x18\x01 \x01(\tB\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
)




_ARGS = _descriptor.Descriptor(
  name='Args',
  full_name='qlua.rpc.getInfoParam.Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='param_name', full_name='qlua.rpc.getInfoParam.Args.param_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=54,
  serialized_end=80,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.getInfoParam.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info_param', full_name='qlua.rpc.getInfoParam.Result.info_param', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=82,
  serialized_end=110,
)

DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Args = _reflection.GeneratedProtocolMessageType('Args', (_message.Message,), dict(
  DESCRIPTOR = _ARGS,
  __module__ = 'qlua.rpc.getInfoParam_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getInfoParam.Args)
  ))
_sym_db.RegisterMessage(Args)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.getInfoParam_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getInfoParam.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
