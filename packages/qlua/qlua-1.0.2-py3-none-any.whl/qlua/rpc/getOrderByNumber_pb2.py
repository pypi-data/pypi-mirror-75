# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/getOrderByNumber.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from qlua.rpc import qlua_structures_pb2 as qlua_dot_rpc_dot_qlua__structures__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='qlua/rpc/getOrderByNumber.proto',
  package='qlua.rpc.getOrderByNumber',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\x1fqlua/rpc/getOrderByNumber.proto\x12\x19qlua.rpc.getOrderByNumber\x1a\x1eqlua/rpc/qlua_structures.proto\",\n\x04\x41rgs\x12\x12\n\nclass_code\x18\x01 \x01(\t\x12\x10\n\x08order_id\x18\x02 \x01(\x03\"_\n\x06Result\x12\"\n\x05order\x18\x01 \x01(\x0b\x32\x13.qlua.structs.Order\x12\x13\n\tnull_indx\x18\x02 \x01(\x08H\x00\x12\x14\n\nvalue_indx\x18\x03 \x01(\x05H\x00\x42\x06\n\x04indxB\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
  ,
  dependencies=[qlua_dot_rpc_dot_qlua__structures__pb2.DESCRIPTOR,])




_ARGS = _descriptor.Descriptor(
  name='Args',
  full_name='qlua.rpc.getOrderByNumber.Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_code', full_name='qlua.rpc.getOrderByNumber.Args.class_code', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_id', full_name='qlua.rpc.getOrderByNumber.Args.order_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=94,
  serialized_end=138,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.getOrderByNumber.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='order', full_name='qlua.rpc.getOrderByNumber.Result.order', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_indx', full_name='qlua.rpc.getOrderByNumber.Result.null_indx', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_indx', full_name='qlua.rpc.getOrderByNumber.Result.value_indx', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
    _descriptor.OneofDescriptor(
      name='indx', full_name='qlua.rpc.getOrderByNumber.Result.indx',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=140,
  serialized_end=235,
)

_RESULT.fields_by_name['order'].message_type = qlua_dot_rpc_dot_qlua__structures__pb2._ORDER
_RESULT.oneofs_by_name['indx'].fields.append(
  _RESULT.fields_by_name['null_indx'])
_RESULT.fields_by_name['null_indx'].containing_oneof = _RESULT.oneofs_by_name['indx']
_RESULT.oneofs_by_name['indx'].fields.append(
  _RESULT.fields_by_name['value_indx'])
_RESULT.fields_by_name['value_indx'].containing_oneof = _RESULT.oneofs_by_name['indx']
DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Args = _reflection.GeneratedProtocolMessageType('Args', (_message.Message,), dict(
  DESCRIPTOR = _ARGS,
  __module__ = 'qlua.rpc.getOrderByNumber_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getOrderByNumber.Args)
  ))
_sym_db.RegisterMessage(Args)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.getOrderByNumber_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getOrderByNumber.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
