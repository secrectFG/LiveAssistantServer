# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngrpc.proto\x12\tLiveProto\"\x07\n\x05\x45mpty\":\n\tStringMsg\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0f\n\x07jsonStr\x18\x02 \x01(\t\x12\x0e\n\x06pbdata\x18\x03 \x01(\x0c\x32\x86\x01\n\x0cLiveMessager\x12;\n\rHandleJsonMsg\x12\x14.LiveProto.StringMsg\x1a\x14.LiveProto.StringMsg\x12\x39\n\rJsonMsgRouter\x12\x10.LiveProto.Empty\x1a\x14.LiveProto.StringMsg0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grpc_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_EMPTY']._serialized_start=25
  _globals['_EMPTY']._serialized_end=32
  _globals['_STRINGMSG']._serialized_start=34
  _globals['_STRINGMSG']._serialized_end=92
  _globals['_LIVEMESSAGER']._serialized_start=95
  _globals['_LIVEMESSAGER']._serialized_end=229
# @@protoc_insertion_point(module_scope)
