# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/InsertRow.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='qlua/rpc/InsertRow.proto',
  package='qlua.rpc.InsertRow',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\x18qlua/rpc/InsertRow.proto\x12\x12qlua.rpc.InsertRow\"!\n\x04\x41rgs\x12\x0c\n\x04t_id\x18\x01 \x01(\x05\x12\x0b\n\x03key\x18\x02 \x01(\x05\"\x18\n\x06Result\x12\x0e\n\x06result\x18\x01 \x01(\x05\x42\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
)




_ARGS = _descriptor.Descriptor(
  name='Args',
  full_name='qlua.rpc.InsertRow.Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='t_id', full_name='qlua.rpc.InsertRow.Args.t_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='key', full_name='qlua.rpc.InsertRow.Args.key', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=48,
  serialized_end=81,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.InsertRow.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='qlua.rpc.InsertRow.Result.result', index=0,
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
  serialized_start=83,
  serialized_end=107,
)

DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Args = _reflection.GeneratedProtocolMessageType('Args', (_message.Message,), dict(
  DESCRIPTOR = _ARGS,
  __module__ = 'qlua.rpc.InsertRow_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.InsertRow.Args)
  ))
_sym_db.RegisterMessage(Args)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.InsertRow_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.InsertRow.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
