# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/datasource/SetUpdateCallback.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='qlua/rpc/datasource/SetUpdateCallback.proto',
  package='qlua.rpc.datasource.SetUpdateCallback',
  syntax='proto3',
  serialized_options=_b('\n\023qlua.rpc.datasourceH\001'),
  serialized_pb=_b('\n+qlua/rpc/datasource/SetUpdateCallback.proto\x12%qlua.rpc.datasource.SetUpdateCallback\"\xc0\x01\n\x04\x41rgs\x12\x17\n\x0f\x64\x61tasource_uuid\x18\x01 \x01(\t\x12\x10\n\x08\x66_cb_def\x18\x02 \x01(\t\x12\x12\n\nwatching_O\x18\x03 \x01(\x08\x12\x12\n\nwatching_H\x18\x04 \x01(\x08\x12\x12\n\nwatching_L\x18\x05 \x01(\x08\x12\x12\n\nwatching_C\x18\x06 \x01(\x08\x12\x12\n\nwatching_V\x18\x07 \x01(\x08\x12\x12\n\nwatching_T\x18\x08 \x01(\x08\x12\x15\n\rwatching_Size\x18\t \x01(\x08\"\x18\n\x06Result\x12\x0e\n\x06result\x18\x01 \x01(\x08\x42\x17\n\x13qlua.rpc.datasourceH\x01\x62\x06proto3')
)




_ARGS = _descriptor.Descriptor(
  name='Args',
  full_name='qlua.rpc.datasource.SetUpdateCallback.Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='datasource_uuid', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.datasource_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='f_cb_def', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.f_cb_def', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watching_O', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.watching_O', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watching_H', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.watching_H', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watching_L', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.watching_L', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watching_C', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.watching_C', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watching_V', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.watching_V', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watching_T', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.watching_T', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watching_Size', full_name='qlua.rpc.datasource.SetUpdateCallback.Args.watching_Size', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=87,
  serialized_end=279,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.datasource.SetUpdateCallback.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='qlua.rpc.datasource.SetUpdateCallback.Result.result', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=281,
  serialized_end=305,
)

DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Args = _reflection.GeneratedProtocolMessageType('Args', (_message.Message,), dict(
  DESCRIPTOR = _ARGS,
  __module__ = 'qlua.rpc.datasource.SetUpdateCallback_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.datasource.SetUpdateCallback.Args)
  ))
_sym_db.RegisterMessage(Args)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.datasource.SetUpdateCallback_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.datasource.SetUpdateCallback.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
