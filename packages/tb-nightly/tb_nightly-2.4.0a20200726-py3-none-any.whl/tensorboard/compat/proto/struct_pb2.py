# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/struct.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import tensor_pb2 as tensorboard_dot_compat_dot_proto_dot_tensor__pb2
from tensorboard.compat.proto import tensor_shape_pb2 as tensorboard_dot_compat_dot_proto_dot_tensor__shape__pb2
from tensorboard.compat.proto import types_pb2 as tensorboard_dot_compat_dot_proto_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorboard/compat/proto/struct.proto',
  package='tensorboard',
  syntax='proto3',
  serialized_options=_b('ZHgithub.com/tensorflow/tensorflow/tensorflow/go/core/core_protos_go_proto'),
  serialized_pb=_b('\n%tensorboard/compat/proto/struct.proto\x12\x0btensorboard\x1a%tensorboard/compat/proto/tensor.proto\x1a+tensorboard/compat/proto/tensor_shape.proto\x1a$tensorboard/compat/proto/types.proto\"\x9a\x05\n\x0fStructuredValue\x12,\n\nnone_value\x18\x01 \x01(\x0b\x32\x16.tensorboard.NoneValueH\x00\x12\x17\n\rfloat64_value\x18\x0b \x01(\x01H\x00\x12\x15\n\x0bint64_value\x18\x0c \x01(\x12H\x00\x12\x16\n\x0cstring_value\x18\r \x01(\tH\x00\x12\x14\n\nbool_value\x18\x0e \x01(\x08H\x00\x12;\n\x12tensor_shape_value\x18\x1f \x01(\x0b\x32\x1d.tensorboard.TensorShapeProtoH\x00\x12\x33\n\x12tensor_dtype_value\x18  \x01(\x0e\x32\x15.tensorboard.DataTypeH\x00\x12\x39\n\x11tensor_spec_value\x18! \x01(\x0b\x32\x1c.tensorboard.TensorSpecProtoH\x00\x12\x35\n\x0ftype_spec_value\x18\" \x01(\x0b\x32\x1a.tensorboard.TypeSpecProtoH\x00\x12H\n\x19\x62ounded_tensor_spec_value\x18# \x01(\x0b\x32#.tensorboard.BoundedTensorSpecProtoH\x00\x12,\n\nlist_value\x18\x33 \x01(\x0b\x32\x16.tensorboard.ListValueH\x00\x12.\n\x0btuple_value\x18\x34 \x01(\x0b\x32\x17.tensorboard.TupleValueH\x00\x12,\n\ndict_value\x18\x35 \x01(\x0b\x32\x16.tensorboard.DictValueH\x00\x12\x39\n\x11named_tuple_value\x18\x36 \x01(\x0b\x32\x1c.tensorboard.NamedTupleValueH\x00\x42\x06\n\x04kind\"\x0b\n\tNoneValue\"9\n\tListValue\x12,\n\x06values\x18\x01 \x03(\x0b\x32\x1c.tensorboard.StructuredValue\":\n\nTupleValue\x12,\n\x06values\x18\x01 \x03(\x0b\x32\x1c.tensorboard.StructuredValue\"\x8c\x01\n\tDictValue\x12\x32\n\x06\x66ields\x18\x01 \x03(\x0b\x32\".tensorboard.DictValue.FieldsEntry\x1aK\n\x0b\x46ieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12+\n\x05value\x18\x02 \x01(\x0b\x32\x1c.tensorboard.StructuredValue:\x02\x38\x01\"E\n\tPairValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12+\n\x05value\x18\x02 \x01(\x0b\x32\x1c.tensorboard.StructuredValue\"G\n\x0fNamedTupleValue\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\x06values\x18\x02 \x03(\x0b\x32\x16.tensorboard.PairValue\"s\n\x0fTensorSpecProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12,\n\x05shape\x18\x02 \x01(\x0b\x32\x1d.tensorboard.TensorShapeProto\x12$\n\x05\x64type\x18\x03 \x01(\x0e\x32\x15.tensorboard.DataType\"\xd0\x01\n\x16\x42oundedTensorSpecProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12,\n\x05shape\x18\x02 \x01(\x0b\x32\x1d.tensorboard.TensorShapeProto\x12$\n\x05\x64type\x18\x03 \x01(\x0e\x32\x15.tensorboard.DataType\x12)\n\x07minimum\x18\x04 \x01(\x0b\x32\x18.tensorboard.TensorProto\x12)\n\x07maximum\x18\x05 \x01(\x0b\x32\x18.tensorboard.TensorProto\"\xa4\x03\n\rTypeSpecProto\x12\x41\n\x0ftype_spec_class\x18\x01 \x01(\x0e\x32(.tensorboard.TypeSpecProto.TypeSpecClass\x12\x30\n\ntype_state\x18\x02 \x01(\x0b\x32\x1c.tensorboard.StructuredValue\x12\x1c\n\x14type_spec_class_name\x18\x03 \x01(\t\"\xff\x01\n\rTypeSpecClass\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x16\n\x12SPARSE_TENSOR_SPEC\x10\x01\x12\x17\n\x13INDEXED_SLICES_SPEC\x10\x02\x12\x16\n\x12RAGGED_TENSOR_SPEC\x10\x03\x12\x15\n\x11TENSOR_ARRAY_SPEC\x10\x04\x12\x15\n\x11\x44\x41TA_DATASET_SPEC\x10\x05\x12\x16\n\x12\x44\x41TA_ITERATOR_SPEC\x10\x06\x12\x11\n\rOPTIONAL_SPEC\x10\x07\x12\x14\n\x10PER_REPLICA_SPEC\x10\x08\x12\x11\n\rVARIABLE_SPEC\x10\t\x12\x16\n\x12ROW_PARTITION_SPEC\x10\nBJZHgithub.com/tensorflow/tensorflow/tensorflow/go/core/core_protos_go_protob\x06proto3')
  ,
  dependencies=[tensorboard_dot_compat_dot_proto_dot_tensor__pb2.DESCRIPTOR,tensorboard_dot_compat_dot_proto_dot_tensor__shape__pb2.DESCRIPTOR,tensorboard_dot_compat_dot_proto_dot_types__pb2.DESCRIPTOR,])



_TYPESPECPROTO_TYPESPECCLASS = _descriptor.EnumDescriptor(
  name='TypeSpecClass',
  full_name='tensorboard.TypeSpecProto.TypeSpecClass',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPARSE_TENSOR_SPEC', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INDEXED_SLICES_SPEC', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RAGGED_TENSOR_SPEC', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TENSOR_ARRAY_SPEC', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DATA_DATASET_SPEC', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DATA_ITERATOR_SPEC', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPTIONAL_SPEC', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PER_REPLICA_SPEC', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VARIABLE_SPEC', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ROW_PARTITION_SPEC', index=10, number=10,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1758,
  serialized_end=2013,
)
_sym_db.RegisterEnumDescriptor(_TYPESPECPROTO_TYPESPECCLASS)


_STRUCTUREDVALUE = _descriptor.Descriptor(
  name='StructuredValue',
  full_name='tensorboard.StructuredValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='none_value', full_name='tensorboard.StructuredValue.none_value', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float64_value', full_name='tensorboard.StructuredValue.float64_value', index=1,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int64_value', full_name='tensorboard.StructuredValue.int64_value', index=2,
      number=12, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_value', full_name='tensorboard.StructuredValue.string_value', index=3,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='tensorboard.StructuredValue.bool_value', index=4,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tensor_shape_value', full_name='tensorboard.StructuredValue.tensor_shape_value', index=5,
      number=31, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tensor_dtype_value', full_name='tensorboard.StructuredValue.tensor_dtype_value', index=6,
      number=32, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tensor_spec_value', full_name='tensorboard.StructuredValue.tensor_spec_value', index=7,
      number=33, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_spec_value', full_name='tensorboard.StructuredValue.type_spec_value', index=8,
      number=34, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bounded_tensor_spec_value', full_name='tensorboard.StructuredValue.bounded_tensor_spec_value', index=9,
      number=35, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='list_value', full_name='tensorboard.StructuredValue.list_value', index=10,
      number=51, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tuple_value', full_name='tensorboard.StructuredValue.tuple_value', index=11,
      number=52, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dict_value', full_name='tensorboard.StructuredValue.dict_value', index=12,
      number=53, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='named_tuple_value', full_name='tensorboard.StructuredValue.named_tuple_value', index=13,
      number=54, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='kind', full_name='tensorboard.StructuredValue.kind',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=177,
  serialized_end=843,
)


_NONEVALUE = _descriptor.Descriptor(
  name='NoneValue',
  full_name='tensorboard.NoneValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=845,
  serialized_end=856,
)


_LISTVALUE = _descriptor.Descriptor(
  name='ListValue',
  full_name='tensorboard.ListValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='tensorboard.ListValue.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=858,
  serialized_end=915,
)


_TUPLEVALUE = _descriptor.Descriptor(
  name='TupleValue',
  full_name='tensorboard.TupleValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='tensorboard.TupleValue.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=917,
  serialized_end=975,
)


_DICTVALUE_FIELDSENTRY = _descriptor.Descriptor(
  name='FieldsEntry',
  full_name='tensorboard.DictValue.FieldsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorboard.DictValue.FieldsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorboard.DictValue.FieldsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1043,
  serialized_end=1118,
)

_DICTVALUE = _descriptor.Descriptor(
  name='DictValue',
  full_name='tensorboard.DictValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fields', full_name='tensorboard.DictValue.fields', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DICTVALUE_FIELDSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=978,
  serialized_end=1118,
)


_PAIRVALUE = _descriptor.Descriptor(
  name='PairValue',
  full_name='tensorboard.PairValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorboard.PairValue.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorboard.PairValue.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=1120,
  serialized_end=1189,
)


_NAMEDTUPLEVALUE = _descriptor.Descriptor(
  name='NamedTupleValue',
  full_name='tensorboard.NamedTupleValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.NamedTupleValue.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='values', full_name='tensorboard.NamedTupleValue.values', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1191,
  serialized_end=1262,
)


_TENSORSPECPROTO = _descriptor.Descriptor(
  name='TensorSpecProto',
  full_name='tensorboard.TensorSpecProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.TensorSpecProto.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorboard.TensorSpecProto.shape', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorboard.TensorSpecProto.dtype', index=2,
      number=3, type=14, cpp_type=8, label=1,
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
  serialized_start=1264,
  serialized_end=1379,
)


_BOUNDEDTENSORSPECPROTO = _descriptor.Descriptor(
  name='BoundedTensorSpecProto',
  full_name='tensorboard.BoundedTensorSpecProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.BoundedTensorSpecProto.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorboard.BoundedTensorSpecProto.shape', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorboard.BoundedTensorSpecProto.dtype', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='minimum', full_name='tensorboard.BoundedTensorSpecProto.minimum', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='maximum', full_name='tensorboard.BoundedTensorSpecProto.maximum', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
  serialized_start=1382,
  serialized_end=1590,
)


_TYPESPECPROTO = _descriptor.Descriptor(
  name='TypeSpecProto',
  full_name='tensorboard.TypeSpecProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type_spec_class', full_name='tensorboard.TypeSpecProto.type_spec_class', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_state', full_name='tensorboard.TypeSpecProto.type_state', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_spec_class_name', full_name='tensorboard.TypeSpecProto.type_spec_class_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TYPESPECPROTO_TYPESPECCLASS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1593,
  serialized_end=2013,
)

_STRUCTUREDVALUE.fields_by_name['none_value'].message_type = _NONEVALUE
_STRUCTUREDVALUE.fields_by_name['tensor_shape_value'].message_type = tensorboard_dot_compat_dot_proto_dot_tensor__shape__pb2._TENSORSHAPEPROTO
_STRUCTUREDVALUE.fields_by_name['tensor_dtype_value'].enum_type = tensorboard_dot_compat_dot_proto_dot_types__pb2._DATATYPE
_STRUCTUREDVALUE.fields_by_name['tensor_spec_value'].message_type = _TENSORSPECPROTO
_STRUCTUREDVALUE.fields_by_name['type_spec_value'].message_type = _TYPESPECPROTO
_STRUCTUREDVALUE.fields_by_name['bounded_tensor_spec_value'].message_type = _BOUNDEDTENSORSPECPROTO
_STRUCTUREDVALUE.fields_by_name['list_value'].message_type = _LISTVALUE
_STRUCTUREDVALUE.fields_by_name['tuple_value'].message_type = _TUPLEVALUE
_STRUCTUREDVALUE.fields_by_name['dict_value'].message_type = _DICTVALUE
_STRUCTUREDVALUE.fields_by_name['named_tuple_value'].message_type = _NAMEDTUPLEVALUE
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['none_value'])
_STRUCTUREDVALUE.fields_by_name['none_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['float64_value'])
_STRUCTUREDVALUE.fields_by_name['float64_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['int64_value'])
_STRUCTUREDVALUE.fields_by_name['int64_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['string_value'])
_STRUCTUREDVALUE.fields_by_name['string_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['bool_value'])
_STRUCTUREDVALUE.fields_by_name['bool_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['tensor_shape_value'])
_STRUCTUREDVALUE.fields_by_name['tensor_shape_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['tensor_dtype_value'])
_STRUCTUREDVALUE.fields_by_name['tensor_dtype_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['tensor_spec_value'])
_STRUCTUREDVALUE.fields_by_name['tensor_spec_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['type_spec_value'])
_STRUCTUREDVALUE.fields_by_name['type_spec_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['bounded_tensor_spec_value'])
_STRUCTUREDVALUE.fields_by_name['bounded_tensor_spec_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['list_value'])
_STRUCTUREDVALUE.fields_by_name['list_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['tuple_value'])
_STRUCTUREDVALUE.fields_by_name['tuple_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['dict_value'])
_STRUCTUREDVALUE.fields_by_name['dict_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_STRUCTUREDVALUE.oneofs_by_name['kind'].fields.append(
  _STRUCTUREDVALUE.fields_by_name['named_tuple_value'])
_STRUCTUREDVALUE.fields_by_name['named_tuple_value'].containing_oneof = _STRUCTUREDVALUE.oneofs_by_name['kind']
_LISTVALUE.fields_by_name['values'].message_type = _STRUCTUREDVALUE
_TUPLEVALUE.fields_by_name['values'].message_type = _STRUCTUREDVALUE
_DICTVALUE_FIELDSENTRY.fields_by_name['value'].message_type = _STRUCTUREDVALUE
_DICTVALUE_FIELDSENTRY.containing_type = _DICTVALUE
_DICTVALUE.fields_by_name['fields'].message_type = _DICTVALUE_FIELDSENTRY
_PAIRVALUE.fields_by_name['value'].message_type = _STRUCTUREDVALUE
_NAMEDTUPLEVALUE.fields_by_name['values'].message_type = _PAIRVALUE
_TENSORSPECPROTO.fields_by_name['shape'].message_type = tensorboard_dot_compat_dot_proto_dot_tensor__shape__pb2._TENSORSHAPEPROTO
_TENSORSPECPROTO.fields_by_name['dtype'].enum_type = tensorboard_dot_compat_dot_proto_dot_types__pb2._DATATYPE
_BOUNDEDTENSORSPECPROTO.fields_by_name['shape'].message_type = tensorboard_dot_compat_dot_proto_dot_tensor__shape__pb2._TENSORSHAPEPROTO
_BOUNDEDTENSORSPECPROTO.fields_by_name['dtype'].enum_type = tensorboard_dot_compat_dot_proto_dot_types__pb2._DATATYPE
_BOUNDEDTENSORSPECPROTO.fields_by_name['minimum'].message_type = tensorboard_dot_compat_dot_proto_dot_tensor__pb2._TENSORPROTO
_BOUNDEDTENSORSPECPROTO.fields_by_name['maximum'].message_type = tensorboard_dot_compat_dot_proto_dot_tensor__pb2._TENSORPROTO
_TYPESPECPROTO.fields_by_name['type_spec_class'].enum_type = _TYPESPECPROTO_TYPESPECCLASS
_TYPESPECPROTO.fields_by_name['type_state'].message_type = _STRUCTUREDVALUE
_TYPESPECPROTO_TYPESPECCLASS.containing_type = _TYPESPECPROTO
DESCRIPTOR.message_types_by_name['StructuredValue'] = _STRUCTUREDVALUE
DESCRIPTOR.message_types_by_name['NoneValue'] = _NONEVALUE
DESCRIPTOR.message_types_by_name['ListValue'] = _LISTVALUE
DESCRIPTOR.message_types_by_name['TupleValue'] = _TUPLEVALUE
DESCRIPTOR.message_types_by_name['DictValue'] = _DICTVALUE
DESCRIPTOR.message_types_by_name['PairValue'] = _PAIRVALUE
DESCRIPTOR.message_types_by_name['NamedTupleValue'] = _NAMEDTUPLEVALUE
DESCRIPTOR.message_types_by_name['TensorSpecProto'] = _TENSORSPECPROTO
DESCRIPTOR.message_types_by_name['BoundedTensorSpecProto'] = _BOUNDEDTENSORSPECPROTO
DESCRIPTOR.message_types_by_name['TypeSpecProto'] = _TYPESPECPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StructuredValue = _reflection.GeneratedProtocolMessageType('StructuredValue', (_message.Message,), {
  'DESCRIPTOR' : _STRUCTUREDVALUE,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.StructuredValue)
  })
_sym_db.RegisterMessage(StructuredValue)

NoneValue = _reflection.GeneratedProtocolMessageType('NoneValue', (_message.Message,), {
  'DESCRIPTOR' : _NONEVALUE,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.NoneValue)
  })
_sym_db.RegisterMessage(NoneValue)

ListValue = _reflection.GeneratedProtocolMessageType('ListValue', (_message.Message,), {
  'DESCRIPTOR' : _LISTVALUE,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.ListValue)
  })
_sym_db.RegisterMessage(ListValue)

TupleValue = _reflection.GeneratedProtocolMessageType('TupleValue', (_message.Message,), {
  'DESCRIPTOR' : _TUPLEVALUE,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.TupleValue)
  })
_sym_db.RegisterMessage(TupleValue)

DictValue = _reflection.GeneratedProtocolMessageType('DictValue', (_message.Message,), {

  'FieldsEntry' : _reflection.GeneratedProtocolMessageType('FieldsEntry', (_message.Message,), {
    'DESCRIPTOR' : _DICTVALUE_FIELDSENTRY,
    '__module__' : 'tensorboard.compat.proto.struct_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.DictValue.FieldsEntry)
    })
  ,
  'DESCRIPTOR' : _DICTVALUE,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.DictValue)
  })
_sym_db.RegisterMessage(DictValue)
_sym_db.RegisterMessage(DictValue.FieldsEntry)

PairValue = _reflection.GeneratedProtocolMessageType('PairValue', (_message.Message,), {
  'DESCRIPTOR' : _PAIRVALUE,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.PairValue)
  })
_sym_db.RegisterMessage(PairValue)

NamedTupleValue = _reflection.GeneratedProtocolMessageType('NamedTupleValue', (_message.Message,), {
  'DESCRIPTOR' : _NAMEDTUPLEVALUE,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.NamedTupleValue)
  })
_sym_db.RegisterMessage(NamedTupleValue)

TensorSpecProto = _reflection.GeneratedProtocolMessageType('TensorSpecProto', (_message.Message,), {
  'DESCRIPTOR' : _TENSORSPECPROTO,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.TensorSpecProto)
  })
_sym_db.RegisterMessage(TensorSpecProto)

BoundedTensorSpecProto = _reflection.GeneratedProtocolMessageType('BoundedTensorSpecProto', (_message.Message,), {
  'DESCRIPTOR' : _BOUNDEDTENSORSPECPROTO,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.BoundedTensorSpecProto)
  })
_sym_db.RegisterMessage(BoundedTensorSpecProto)

TypeSpecProto = _reflection.GeneratedProtocolMessageType('TypeSpecProto', (_message.Message,), {
  'DESCRIPTOR' : _TYPESPECPROTO,
  '__module__' : 'tensorboard.compat.proto.struct_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.TypeSpecProto)
  })
_sym_db.RegisterMessage(TypeSpecProto)


DESCRIPTOR._options = None
_DICTVALUE_FIELDSENTRY._options = None
# @@protoc_insertion_point(module_scope)
