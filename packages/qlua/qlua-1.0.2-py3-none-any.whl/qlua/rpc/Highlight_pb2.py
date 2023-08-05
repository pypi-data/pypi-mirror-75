# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qlua/rpc/Highlight.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='qlua/rpc/Highlight.proto',
  package='qlua.rpc.Highlight',
  syntax='proto3',
  serialized_options=_b('\n\010qlua.rpcH\001'),
  serialized_pb=_b('\n\x18qlua/rpc/Highlight.proto\x12\x12qlua.rpc.Highlight\"\xfd\x01\n\x04\x41rgs\x12\x0c\n\x04t_id\x18\x01 \x01(\x05\x12\x12\n\x08null_row\x18\x02 \x01(\x08H\x00\x12\x13\n\tvalue_row\x18\x03 \x01(\rH\x00\x12\x12\n\x08null_col\x18\x04 \x01(\x08H\x01\x12\x13\n\tvalue_col\x18\x05 \x01(\rH\x01\x12\x16\n\x0cnull_b_color\x18\x06 \x01(\x08H\x02\x12\x17\n\rvalue_b_color\x18\x07 \x01(\x05H\x02\x12\x16\n\x0cnull_f_color\x18\x08 \x01(\x08H\x03\x12\x17\n\rvalue_f_color\x18\t \x01(\x05H\x03\x12\x0f\n\x07timeout\x18\n \x01(\x04\x42\x05\n\x03rowB\x05\n\x03\x63olB\t\n\x07\x62_colorB\t\n\x07\x66_color\"\x18\n\x06Result\x12\x0e\n\x06result\x18\x01 \x01(\x08\x42\x0c\n\x08qlua.rpcH\x01\x62\x06proto3')
)




_ARGS = _descriptor.Descriptor(
  name='Args',
  full_name='qlua.rpc.Highlight.Args',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='t_id', full_name='qlua.rpc.Highlight.Args.t_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_row', full_name='qlua.rpc.Highlight.Args.null_row', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_row', full_name='qlua.rpc.Highlight.Args.value_row', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_col', full_name='qlua.rpc.Highlight.Args.null_col', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_col', full_name='qlua.rpc.Highlight.Args.value_col', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_b_color', full_name='qlua.rpc.Highlight.Args.null_b_color', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_b_color', full_name='qlua.rpc.Highlight.Args.value_b_color', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_f_color', full_name='qlua.rpc.Highlight.Args.null_f_color', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value_f_color', full_name='qlua.rpc.Highlight.Args.value_f_color', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='qlua.rpc.Highlight.Args.timeout', index=9,
      number=10, type=4, cpp_type=4, label=1,
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
      name='row', full_name='qlua.rpc.Highlight.Args.row',
      index=0, containing_type=None, fields=[]),
    _descriptor.OneofDescriptor(
      name='col', full_name='qlua.rpc.Highlight.Args.col',
      index=1, containing_type=None, fields=[]),
    _descriptor.OneofDescriptor(
      name='b_color', full_name='qlua.rpc.Highlight.Args.b_color',
      index=2, containing_type=None, fields=[]),
    _descriptor.OneofDescriptor(
      name='f_color', full_name='qlua.rpc.Highlight.Args.f_color',
      index=3, containing_type=None, fields=[]),
  ],
  serialized_start=49,
  serialized_end=302,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='qlua.rpc.Highlight.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='qlua.rpc.Highlight.Result.result', index=0,
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
  serialized_start=304,
  serialized_end=328,
)

_ARGS.oneofs_by_name['row'].fields.append(
  _ARGS.fields_by_name['null_row'])
_ARGS.fields_by_name['null_row'].containing_oneof = _ARGS.oneofs_by_name['row']
_ARGS.oneofs_by_name['row'].fields.append(
  _ARGS.fields_by_name['value_row'])
_ARGS.fields_by_name['value_row'].containing_oneof = _ARGS.oneofs_by_name['row']
_ARGS.oneofs_by_name['col'].fields.append(
  _ARGS.fields_by_name['null_col'])
_ARGS.fields_by_name['null_col'].containing_oneof = _ARGS.oneofs_by_name['col']
_ARGS.oneofs_by_name['col'].fields.append(
  _ARGS.fields_by_name['value_col'])
_ARGS.fields_by_name['value_col'].containing_oneof = _ARGS.oneofs_by_name['col']
_ARGS.oneofs_by_name['b_color'].fields.append(
  _ARGS.fields_by_name['null_b_color'])
_ARGS.fields_by_name['null_b_color'].containing_oneof = _ARGS.oneofs_by_name['b_color']
_ARGS.oneofs_by_name['b_color'].fields.append(
  _ARGS.fields_by_name['value_b_color'])
_ARGS.fields_by_name['value_b_color'].containing_oneof = _ARGS.oneofs_by_name['b_color']
_ARGS.oneofs_by_name['f_color'].fields.append(
  _ARGS.fields_by_name['null_f_color'])
_ARGS.fields_by_name['null_f_color'].containing_oneof = _ARGS.oneofs_by_name['f_color']
_ARGS.oneofs_by_name['f_color'].fields.append(
  _ARGS.fields_by_name['value_f_color'])
_ARGS.fields_by_name['value_f_color'].containing_oneof = _ARGS.oneofs_by_name['f_color']
DESCRIPTOR.message_types_by_name['Args'] = _ARGS
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Args = _reflection.GeneratedProtocolMessageType('Args', (_message.Message,), dict(
  DESCRIPTOR = _ARGS,
  __module__ = 'qlua.rpc.Highlight_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.Highlight.Args)
  ))
_sym_db.RegisterMessage(Args)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), dict(
  DESCRIPTOR = _RESULT,
  __module__ = 'qlua.rpc.Highlight_pb2'
  # @@protoc_insertion_point(class_scope:qlua.rpc.Highlight.Result)
  ))
_sym_db.RegisterMessage(Result)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
