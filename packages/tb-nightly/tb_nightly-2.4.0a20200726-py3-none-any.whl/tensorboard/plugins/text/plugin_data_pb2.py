# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/plugins/text/plugin_data.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorboard/plugins/text/plugin_data.proto',
  package='tensorboard',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n*tensorboard/plugins/text/plugin_data.proto\x12\x0btensorboard\"!\n\x0eTextPluginData\x12\x0f\n\x07version\x18\x01 \x01(\x05\x62\x06proto3')
)




_TEXTPLUGINDATA = _descriptor.Descriptor(
  name='TextPluginData',
  full_name='tensorboard.TextPluginData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='tensorboard.TextPluginData.version', index=0,
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
  serialized_start=59,
  serialized_end=92,
)

DESCRIPTOR.message_types_by_name['TextPluginData'] = _TEXTPLUGINDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TextPluginData = _reflection.GeneratedProtocolMessageType('TextPluginData', (_message.Message,), {
  'DESCRIPTOR' : _TEXTPLUGINDATA,
  '__module__' : 'tensorboard.plugins.text.plugin_data_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.TextPluginData)
  })
_sym_db.RegisterMessage(TextPluginData)


# @@protoc_insertion_point(module_scope)
