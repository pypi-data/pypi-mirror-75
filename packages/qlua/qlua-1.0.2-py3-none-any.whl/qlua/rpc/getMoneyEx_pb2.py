# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/getMoneyEx.proto

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
  name='qlua/rpc/getMoneyEx.proto',
  package='qlua.rpc.getMoneyEx',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\x19qlua/rpc/getMoneyEx.proto\x12\x13qlua.rpc.getMoneyEx\x1a\x1eqlua/rpc/qlua_structures.proto\"^\n\x04\x41rgs\x12\x0e\n\x06\x66irmid\x18\x01 \x01(\t\x12\x13\n\x0b\x63lient_code\x18\x02 \x01(\t\x12\x0b\n\x03tag\x18\x03 \x01(\t\x12\x10\n\x08\x63urrcode\x18\x04 \x01(\t\x12\x12\n\nlimit_kind\x18\x05 \x01(\x05\"4\n\x06Result\x12*\n\x08money_ex\x18\x01 \x01(\x0b\x32\x18.qlua.structs.MoneyLimitB\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
  ,
  dependencies=[qlua_dot_rpc_dot_qlua__structures__pb2.DESCRIPTOR,])




_ARGS = _descriptor.Descriptor(
  name='Args',
  full_name='qlua.rpc.getMoneyEx.Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='firmid', full_name='qlua.rpc.getMoneyEx.Args.firmid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_code', full_name='qlua.rpc.getMoneyEx.Args.client_code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tag', full_name='qlua.rpc.getMoneyEx.Args.tag', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='currcode', full_name='qlua.rpc.getMoneyEx.Args.currcode', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='limit_kind', full_name='qlua.rpc.getMoneyEx.Args.limit_kind', index=4,
      number=5, type=5, cpp_type=1, label=1,
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
  serialized_start=82,
  serialized_end=176,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.getMoneyEx.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='money_ex', full_name='qlua.rpc.getMoneyEx.Result.money_ex', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=178,
  serialized_end=230,
)

_RESULT.fields_by_name['money_ex'].message_type = qlua_dot_rpc_dot_qlua__structures__pb2._MONEYLIMIT
DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Args = _reflection.GeneratedProtocolMessageType('Args', (_message.Message,), dict(
  DESCRIPTOR = _ARGS,
  __module__ = 'qlua.rpc.getMoneyEx_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getMoneyEx.Args)
  ))
_sym_db.RegisterMessage(Args)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.getMoneyEx_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.getMoneyEx.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
