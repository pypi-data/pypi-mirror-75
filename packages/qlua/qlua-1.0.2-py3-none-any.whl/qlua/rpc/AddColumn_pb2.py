# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/AddColumn.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='qlua/rpc/AddColumn.proto',
  package='qlua.rpc.AddColumn',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\x18qlua/rpc/AddColumn.proto\x12\x12qlua.rpc.AddColumn\"\x8f\x01\n\x04\x41rgs\x12\x0c\n\x04t_id\x18\x01 \x01(\x05\x12\r\n\x05icode\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nis_default\x18\x04 \x01(\x08\x12\x39\n\x08par_type\x18\x05 \x01(\x0e\x32\'.qlua.rpc.AddColumn.ColumnParameterType\x12\r\n\x05width\x18\x06 \x01(\x05\"\x18\n\x06Result\x12\x0e\n\x06result\x18\x01 \x01(\x05*\xcb\x01\n\x13\x43olumnParameterType\x12\r\n\tUNDEFINED\x10\x00\x12\x13\n\x0fQTABLE_INT_TYPE\x10\x01\x12\x16\n\x12QTABLE_DOUBLE_TYPE\x10\x02\x12\x15\n\x11QTABLE_INT64_TYPE\x10\x03\x12\x1d\n\x19QTABLE_CACHED_STRING_TYPE\x10\x04\x12\x14\n\x10QTABLE_TIME_TYPE\x10\x05\x12\x14\n\x10QTABLE_DATE_TYPE\x10\x06\x12\x16\n\x12QTABLE_STRING_TYPE\x10\x07\x42\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
)

_COLUMNPARAMETERTYPE = _descriptor.EnumDescriptor(
  name='ColumnParameterType',
  full_name='qlua.rpc.AddColumn.ColumnParameterType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QTABLE_INT_TYPE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QTABLE_DOUBLE_TYPE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QTABLE_INT64_TYPE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QTABLE_CACHED_STRING_TYPE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QTABLE_TIME_TYPE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QTABLE_DATE_TYPE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QTABLE_STRING_TYPE', index=7, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=221,
  serialized_end=424,
)
_sym_db.RegisterEnumDescriptor(_COLUMNPARAMETERTYPE)

ColumnParameterType = enum_type_wrapper.EnumTypeWrapper(_COLUMNPARAMETERTYPE)
UNDEFINED = 0
QTABLE_INT_TYPE = 1
QTABLE_DOUBLE_TYPE = 2
QTABLE_INT64_TYPE = 3
QTABLE_CACHED_STRING_TYPE = 4
QTABLE_TIME_TYPE = 5
QTABLE_DATE_TYPE = 6
QTABLE_STRING_TYPE = 7



_ARGS = _descriptor.Descriptor(
  name='Args',
  full_name='qlua.rpc.AddColumn.Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='t_id', full_name='qlua.rpc.AddColumn.Args.t_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='icode', full_name='qlua.rpc.AddColumn.Args.icode', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='qlua.rpc.AddColumn.Args.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_default', full_name='qlua.rpc.AddColumn.Args.is_default', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='par_type', full_name='qlua.rpc.AddColumn.Args.par_type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='width', full_name='qlua.rpc.AddColumn.Args.width', index=5,
      number=6, type=5, cpp_type=1, label=1,
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
  serialized_start=49,
  serialized_end=192,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.AddColumn.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='qlua.rpc.AddColumn.Result.result', index=0,
      number=1, type=5, cpp_type=1, label=1,
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
  serialized_start=194,
  serialized_end=218,
)

_ARGS.fields_by_name['par_type'].enum_type = _COLUMNPARAMETERTYPE
DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
DESCRIPTOR.enum_types_by_name['ColumnParameterType'] = _COLUMNPARAMETERTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Args = _reflection.GeneratedProtocolMessageType('Args', (_message.Message,), dict(
  DESCRIPTOR = _ARGS,
  __module__ = 'qlua.rpc.AddColumn_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.AddColumn.Args)
  ))
_sym_db.RegisterMessage(Args)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.AddColumn_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.AddColumn.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
