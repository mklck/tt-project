# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngame.proto\x12\x04game\"\x1b\n\x03Hit\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\"e\n\x07Request\x12\r\n\x05token\x18\x01 \x01(\x05\x12\x1a\n\x04type\x18\x02 \x01(\x0e\x32\x0c.game.RqType\x12\x0e\n\x04name\x18\x03 \x01(\tH\x00\x12\x18\n\x03hit\x18\x04 \x01(\x0b\x32\t.game.HitH\x00\x42\x05\n\x03req\"h\n\x08Response\x12\r\n\x05token\x18\x01 \x01(\x05\x12\x1a\n\x04type\x18\x02 \x01(\x0e\x32\x0c.game.RsType\x12\x10\n\x06youWon\x18\x03 \x01(\x08H\x00\x12\x18\n\x03hit\x18\x04 \x01(\x0b\x32\t.game.HitH\x00\x42\x05\n\x03res*4\n\x06RqType\x12\x0f\n\x0bRQ_REGISTER\x10\x00\x12\r\n\tRQ_UPDATE\x10\x01\x12\n\n\x06RQ_HIT\x10\x02*5\n\x06RsType\x12\n\n\x06RS_HIT\x10\x00\x12\t\n\x05RS_OK\x10\x01\x12\x14\n\x10RS_INVALID_VALUE\x10\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'game_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RQTYPE']._serialized_start=258
  _globals['_RQTYPE']._serialized_end=310
  _globals['_RSTYPE']._serialized_start=312
  _globals['_RSTYPE']._serialized_end=365
  _globals['_HIT']._serialized_start=20
  _globals['_HIT']._serialized_end=47
  _globals['_REQUEST']._serialized_start=49
  _globals['_REQUEST']._serialized_end=150
  _globals['_RESPONSE']._serialized_start=152
  _globals['_RESPONSE']._serialized_end=256
# @@protoc_insertion_point(module_scope)
