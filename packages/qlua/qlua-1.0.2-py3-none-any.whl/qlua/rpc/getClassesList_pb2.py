# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/getClassesList.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='qlua/rpc/getClassesList.proto',
  package='qlua.rpc.getClassesList',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\x1dqlua/rpc/getClassesList.proto\x12\x17qlua.rpc.getClassesList\"\x1e\n\x06Result\x12\x14\n\x0c\x63lasses_list\x18\x01 \x01(\tB\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
)




_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.getClassesList.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='classes_list', full_name='qlua.rpc.getClassesList.Result.classes_list', index=0,
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
  serialized_start=58,
  serialized_end=88,
)

DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.getClassesList_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getClassesList.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
