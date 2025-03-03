# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: subtrace_pubsub.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15subtrace_pubsub.proto\x12\x0fsubtrace.pubsub\"\x90\x01\n\rJoinPublisher\x1a=\n\x07Request\x12\x1d\n\x10link_id_override\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x13\n\x11_link_id_override\x1a@\n\x08Response\x12\x13\n\x05\x65rror\x18\xe8\x07 \x01(\tH\x00\x88\x01\x01\x12\x15\n\rwebsocket_url\x18\x01 \x01(\tB\x08\n\x06_error\"\x89\x01\n\x0eJoinSubscriber\x1a\x35\n\x07Request\x12\x19\n\x0cnamespace_id\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x0f\n\r_namespace_id\x1a@\n\x08Response\x12\x13\n\x05\x65rror\x18\xe8\x07 \x01(\tH\x00\x88\x01\x01\x12\x15\n\rwebsocket_url\x18\x01 \x01(\tB\x08\n\x06_error\"\x92\x02\n\x05\x45vent\x12\x30\n\x0b\x63oncrete_v1\x18\x01 \x01(\x0b\x32\x19.subtrace.pubsub.Event.V1H\x00\x1a#\n\x03Log\x12\r\n\x05lines\x18\x01 \x03(\t\x12\r\n\x05index\x18\x02 \x01(\x04\x1a\xa5\x01\n\x02V1\x12\x31\n\x04tags\x18\x01 \x03(\x0b\x32#.subtrace.pubsub.Event.V1.TagsEntry\x12\x16\n\x0ehar_entry_json\x18\x02 \x01(\x0c\x12\'\n\x03log\x18\x03 \x01(\x0b\x32\x1a.subtrace.pubsub.Event.Log\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\n\n\x08\x63oncrete\"\xd5\x02\n\x13SetSubscriberConfig\x12>\n\x0b\x63oncrete_v1\x18\x01 \x01(\x0b\x32\'.subtrace.pubsub.SetSubscriberConfig.V1H\x00\x1a\xf1\x01\n\x02V1\x12<\n\x04\x63\x61ll\x18\x01 \x01(\x0b\x32,.subtrace.pubsub.SetSubscriberConfig.V1.CallH\x00\x12@\n\x06result\x18\x02 \x01(\x0b\x32..subtrace.pubsub.SetSubscriberConfig.V1.ResultH\x00\x1a)\n\x04\x43\x61ll\x12\x10\n\x08revision\x18\x01 \x01(\x04\x12\x0f\n\x07\x66ilters\x18\x02 \x03(\t\x1a\x38\n\x06Result\x12\x10\n\x08revision\x18\x01 \x01(\x04\x12\x12\n\x05\x65rror\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_errorB\x06\n\x04typeB\n\n\x08\x63oncrete\"\x8c\x01\n\rAnnounceStats\x12\x38\n\x0b\x63oncrete_v1\x18\x01 \x01(\x0b\x32!.subtrace.pubsub.AnnounceStats.V1H\x00\x1a\x35\n\x02V1\x12\x16\n\x0enum_publishers\x18\x01 \x01(\x04\x12\x17\n\x0fnum_subscribers\x18\x02 \x01(\x04\x42\n\n\x08\x63oncrete\"\x88\x02\n\x07Message\x12\x32\n\x0b\x63oncrete_v1\x18\x01 \x01(\x0b\x32\x1b.subtrace.pubsub.Message.V1H\x00\x1a\xbc\x01\n\x02V1\x12\'\n\x05\x65vent\x18\x01 \x01(\x0b\x32\x16.subtrace.pubsub.EventH\x00\x12\x45\n\x15set_subscriber_config\x18\x02 \x01(\x0b\x32$.subtrace.pubsub.SetSubscriberConfigH\x00\x12\x38\n\x0e\x61nnounce_stats\x18\x03 \x01(\x0b\x32\x1e.subtrace.pubsub.AnnounceStatsH\x00\x42\x0c\n\nunderlyingB\n\n\x08\x63oncreteB\x15Z\x13subtrace.dev/pubsubb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'subtrace_pubsub_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\023subtrace.dev/pubsub'
  _EVENT_V1_TAGSENTRY._options = None
  _EVENT_V1_TAGSENTRY._serialized_options = b'8\001'
  _JOINPUBLISHER._serialized_start=43
  _JOINPUBLISHER._serialized_end=187
  _JOINPUBLISHER_REQUEST._serialized_start=60
  _JOINPUBLISHER_REQUEST._serialized_end=121
  _JOINPUBLISHER_RESPONSE._serialized_start=123
  _JOINPUBLISHER_RESPONSE._serialized_end=187
  _JOINSUBSCRIBER._serialized_start=190
  _JOINSUBSCRIBER._serialized_end=327
  _JOINSUBSCRIBER_REQUEST._serialized_start=208
  _JOINSUBSCRIBER_REQUEST._serialized_end=261
  _JOINSUBSCRIBER_RESPONSE._serialized_start=123
  _JOINSUBSCRIBER_RESPONSE._serialized_end=187
  _EVENT._serialized_start=330
  _EVENT._serialized_end=604
  _EVENT_LOG._serialized_start=389
  _EVENT_LOG._serialized_end=424
  _EVENT_V1._serialized_start=427
  _EVENT_V1._serialized_end=592
  _EVENT_V1_TAGSENTRY._serialized_start=549
  _EVENT_V1_TAGSENTRY._serialized_end=592
  _SETSUBSCRIBERCONFIG._serialized_start=607
  _SETSUBSCRIBERCONFIG._serialized_end=948
  _SETSUBSCRIBERCONFIG_V1._serialized_start=695
  _SETSUBSCRIBERCONFIG_V1._serialized_end=936
  _SETSUBSCRIBERCONFIG_V1_CALL._serialized_start=829
  _SETSUBSCRIBERCONFIG_V1_CALL._serialized_end=870
  _SETSUBSCRIBERCONFIG_V1_RESULT._serialized_start=872
  _SETSUBSCRIBERCONFIG_V1_RESULT._serialized_end=928
  _ANNOUNCESTATS._serialized_start=951
  _ANNOUNCESTATS._serialized_end=1091
  _ANNOUNCESTATS_V1._serialized_start=1026
  _ANNOUNCESTATS_V1._serialized_end=1079
  _MESSAGE._serialized_start=1094
  _MESSAGE._serialized_end=1358
  _MESSAGE_V1._serialized_start=1158
  _MESSAGE_V1._serialized_end=1346
# @@protoc_insertion_point(module_scope)
