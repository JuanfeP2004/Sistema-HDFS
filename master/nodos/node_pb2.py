# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: node.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'node.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nnode.proto\"#\n\x0e\x43ommandRequest\x12\x11\n\tparameter\x18\x01 \x01(\t\"\x1f\n\x0c\x43ommandReply\x12\x0f\n\x07message\x18\x01 \x01(\t2\xad\x01\n\x08\x43ommands\x12%\n\x03Get\x12\x0f.CommandRequest\x1a\r.CommandReply\x12%\n\x03Put\x12\x0f.CommandRequest\x1a\r.CommandReply\x12(\n\x06Remove\x12\x0f.CommandRequest\x1a\r.CommandReply\x12)\n\x07GetInfo\x12\x0f.CommandRequest\x1a\r.CommandReplyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'node_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_COMMANDREQUEST']._serialized_start=14
  _globals['_COMMANDREQUEST']._serialized_end=49
  _globals['_COMMANDREPLY']._serialized_start=51
  _globals['_COMMANDREPLY']._serialized_end=82
  _globals['_COMMANDS']._serialized_start=85
  _globals['_COMMANDS']._serialized_end=258
# @@protoc_insertion_point(module_scope)
