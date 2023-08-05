# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: network_packet.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='network_packet.proto',
  package='optilab.optnet',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14network_packet.proto\x12\x0eoptilab.optnet\"\xc1\x01\n\x19NetworkProtoPacketPayload\x12\x12\n\x08p_double\x18\x01 \x01(\x01H\x00\x12\x11\n\x07p_float\x18\x02 \x01(\x02H\x00\x12\x11\n\x07p_int32\x18\x03 \x01(\x05H\x00\x12\x11\n\x07p_int64\x18\x04 \x01(\x03H\x00\x12\x12\n\x08p_uint32\x18\x05 \x01(\rH\x00\x12\x12\n\x08p_uint64\x18\x06 \x01(\x04H\x00\x12\x10\n\x06p_bool\x18\x07 \x01(\x08H\x00\x12\x12\n\x08p_string\x18\x08 \x01(\tH\x00\x42\t\n\x07payload\"\x96\x02\n\x12NetworkProtoPacket\x12<\n\x0bpayloadType\x18\x01 \x01(\x0e\x32\'.optilab.optnet.NetworkProtoPacket.Type\x12:\n\x07payload\x18\x02 \x03(\x0b\x32).optilab.optnet.NetworkProtoPacketPayload\"\x85\x01\n\x04Type\x12\x0e\n\nNPT_DOUBLE\x10\x00\x12\r\n\tNPT_FLOAT\x10\x01\x12\x0e\n\nNPT_INT_32\x10\x02\x12\x0e\n\nNPT_INT_64\x10\x03\x12\x0f\n\x0bNPT_UINT_32\x10\x04\x12\x0f\n\x0bNPT_UINT_64\x10\x05\x12\x0c\n\x08NPT_BOOL\x10\x06\x12\x0e\n\nNPT_STRING\x10\x07\"\xa3\x02\n\x17PointToPointProtoPacket\x12@\n\npacketType\x18\x01 \x01(\x0e\x32,.optilab.optnet.PointToPointProtoPacket.Type\x12\x10\n\x08packetId\x18\x02 \x01(\x03\x12\x0f\n\x07payload\x18\x03 \x01(\x0c\x12\x13\n\x0bpayloadType\x18\x04 \x01(\x05\x12\x12\n\nsourceRoot\x18\x05 \x01(\x08\x12\x11\n\tpacketTag\x18\x06 \x01(\x05\"g\n\x04Type\x12\x13\n\x0fHubRegistration\x10\x00\x12\x15\n\x11HubUnregistration\x10\x01\x12\x17\n\x13PointToPointPayload\x10\x02\x12\x1a\n\x16NetworkSynchronization\x10\x03\"\xcd\x03\n\x14\x42roadcastProtoPacket\x12=\n\npacketType\x18\x01 \x01(\x0e\x32).optilab.optnet.BroadcastProtoPacket.Type\x12\x0f\n\x07payload\x18\x02 \x01(\x0c\x12\x13\n\x0bpayloadType\x18\x03 \x01(\x05\x12H\n\nnetworkMap\x18\x04 \x03(\x0b\x32\x34.optilab.optnet.BroadcastProtoPacket.NetworkMapEntry\x12\x12\n\nsourceAddr\x18\x05 \x01(\x0c\x1a\x39\n\x13ProtoNetworkAddress\x12\x10\n\x08sendAddr\x18\x01 \x01(\x0c\x12\x10\n\x08recvAddr\x18\x02 \x01(\x0c\x1ak\n\x0fNetworkMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12G\n\x05value\x18\x02 \x01(\x0b\x32\x38.optilab.optnet.BroadcastProtoPacket.ProtoNetworkAddress:\x02\x38\x01\"J\n\x04Type\x12\x14\n\x10\x42roadcastPayload\x10\x00\x12\x1a\n\x16NetworkSynchronization\x10\x01\x12\x10\n\x0cNetworkAbort\x10\x02\x62\x06proto3'
)



_NETWORKPROTOPACKET_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='optilab.optnet.NetworkProtoPacket.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NPT_DOUBLE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NPT_FLOAT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NPT_INT_32', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NPT_INT_64', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NPT_UINT_32', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NPT_UINT_64', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NPT_BOOL', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NPT_STRING', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=382,
  serialized_end=515,
)
_sym_db.RegisterEnumDescriptor(_NETWORKPROTOPACKET_TYPE)

_POINTTOPOINTPROTOPACKET_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='optilab.optnet.PointToPointProtoPacket.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HubRegistration', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HubUnregistration', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PointToPointPayload', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NetworkSynchronization', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=706,
  serialized_end=809,
)
_sym_db.RegisterEnumDescriptor(_POINTTOPOINTPROTOPACKET_TYPE)

_BROADCASTPROTOPACKET_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='optilab.optnet.BroadcastProtoPacket.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BroadcastPayload', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NetworkSynchronization', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NetworkAbort', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1199,
  serialized_end=1273,
)
_sym_db.RegisterEnumDescriptor(_BROADCASTPROTOPACKET_TYPE)


_NETWORKPROTOPACKETPAYLOAD = _descriptor.Descriptor(
  name='NetworkProtoPacketPayload',
  full_name='optilab.optnet.NetworkProtoPacketPayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='p_double', full_name='optilab.optnet.NetworkProtoPacketPayload.p_double', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='p_float', full_name='optilab.optnet.NetworkProtoPacketPayload.p_float', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='p_int32', full_name='optilab.optnet.NetworkProtoPacketPayload.p_int32', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='p_int64', full_name='optilab.optnet.NetworkProtoPacketPayload.p_int64', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='p_uint32', full_name='optilab.optnet.NetworkProtoPacketPayload.p_uint32', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='p_uint64', full_name='optilab.optnet.NetworkProtoPacketPayload.p_uint64', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='p_bool', full_name='optilab.optnet.NetworkProtoPacketPayload.p_bool', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='p_string', full_name='optilab.optnet.NetworkProtoPacketPayload.p_string', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
      name='payload', full_name='optilab.optnet.NetworkProtoPacketPayload.payload',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=41,
  serialized_end=234,
)


_NETWORKPROTOPACKET = _descriptor.Descriptor(
  name='NetworkProtoPacket',
  full_name='optilab.optnet.NetworkProtoPacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='payloadType', full_name='optilab.optnet.NetworkProtoPacket.payloadType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='optilab.optnet.NetworkProtoPacket.payload', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _NETWORKPROTOPACKET_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=237,
  serialized_end=515,
)


_POINTTOPOINTPROTOPACKET = _descriptor.Descriptor(
  name='PointToPointProtoPacket',
  full_name='optilab.optnet.PointToPointProtoPacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='packetType', full_name='optilab.optnet.PointToPointProtoPacket.packetType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='packetId', full_name='optilab.optnet.PointToPointProtoPacket.packetId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='optilab.optnet.PointToPointProtoPacket.payload', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payloadType', full_name='optilab.optnet.PointToPointProtoPacket.payloadType', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sourceRoot', full_name='optilab.optnet.PointToPointProtoPacket.sourceRoot', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='packetTag', full_name='optilab.optnet.PointToPointProtoPacket.packetTag', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _POINTTOPOINTPROTOPACKET_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=518,
  serialized_end=809,
)


_BROADCASTPROTOPACKET_PROTONETWORKADDRESS = _descriptor.Descriptor(
  name='ProtoNetworkAddress',
  full_name='optilab.optnet.BroadcastProtoPacket.ProtoNetworkAddress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sendAddr', full_name='optilab.optnet.BroadcastProtoPacket.ProtoNetworkAddress.sendAddr', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='recvAddr', full_name='optilab.optnet.BroadcastProtoPacket.ProtoNetworkAddress.recvAddr', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1031,
  serialized_end=1088,
)

_BROADCASTPROTOPACKET_NETWORKMAPENTRY = _descriptor.Descriptor(
  name='NetworkMapEntry',
  full_name='optilab.optnet.BroadcastProtoPacket.NetworkMapEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='optilab.optnet.BroadcastProtoPacket.NetworkMapEntry.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='optilab.optnet.BroadcastProtoPacket.NetworkMapEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1090,
  serialized_end=1197,
)

_BROADCASTPROTOPACKET = _descriptor.Descriptor(
  name='BroadcastProtoPacket',
  full_name='optilab.optnet.BroadcastProtoPacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='packetType', full_name='optilab.optnet.BroadcastProtoPacket.packetType', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='optilab.optnet.BroadcastProtoPacket.payload', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payloadType', full_name='optilab.optnet.BroadcastProtoPacket.payloadType', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='networkMap', full_name='optilab.optnet.BroadcastProtoPacket.networkMap', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sourceAddr', full_name='optilab.optnet.BroadcastProtoPacket.sourceAddr', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_BROADCASTPROTOPACKET_PROTONETWORKADDRESS, _BROADCASTPROTOPACKET_NETWORKMAPENTRY, ],
  enum_types=[
    _BROADCASTPROTOPACKET_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=812,
  serialized_end=1273,
)

_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_double'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_double'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_float'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_float'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_int32'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_int32'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_int64'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_int64'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_uint32'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_uint32'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_uint64'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_uint64'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_bool'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_bool'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload'].fields.append(
  _NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_string'])
_NETWORKPROTOPACKETPAYLOAD.fields_by_name['p_string'].containing_oneof = _NETWORKPROTOPACKETPAYLOAD.oneofs_by_name['payload']
_NETWORKPROTOPACKET.fields_by_name['payloadType'].enum_type = _NETWORKPROTOPACKET_TYPE
_NETWORKPROTOPACKET.fields_by_name['payload'].message_type = _NETWORKPROTOPACKETPAYLOAD
_NETWORKPROTOPACKET_TYPE.containing_type = _NETWORKPROTOPACKET
_POINTTOPOINTPROTOPACKET.fields_by_name['packetType'].enum_type = _POINTTOPOINTPROTOPACKET_TYPE
_POINTTOPOINTPROTOPACKET_TYPE.containing_type = _POINTTOPOINTPROTOPACKET
_BROADCASTPROTOPACKET_PROTONETWORKADDRESS.containing_type = _BROADCASTPROTOPACKET
_BROADCASTPROTOPACKET_NETWORKMAPENTRY.fields_by_name['value'].message_type = _BROADCASTPROTOPACKET_PROTONETWORKADDRESS
_BROADCASTPROTOPACKET_NETWORKMAPENTRY.containing_type = _BROADCASTPROTOPACKET
_BROADCASTPROTOPACKET.fields_by_name['packetType'].enum_type = _BROADCASTPROTOPACKET_TYPE
_BROADCASTPROTOPACKET.fields_by_name['networkMap'].message_type = _BROADCASTPROTOPACKET_NETWORKMAPENTRY
_BROADCASTPROTOPACKET_TYPE.containing_type = _BROADCASTPROTOPACKET
DESCRIPTOR.message_types_by_name['NetworkProtoPacketPayload'] = _NETWORKPROTOPACKETPAYLOAD
DESCRIPTOR.message_types_by_name['NetworkProtoPacket'] = _NETWORKPROTOPACKET
DESCRIPTOR.message_types_by_name['PointToPointProtoPacket'] = _POINTTOPOINTPROTOPACKET
DESCRIPTOR.message_types_by_name['BroadcastProtoPacket'] = _BROADCASTPROTOPACKET
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NetworkProtoPacketPayload = _reflection.GeneratedProtocolMessageType('NetworkProtoPacketPayload', (_message.Message,), {
  'DESCRIPTOR' : _NETWORKPROTOPACKETPAYLOAD,
  '__module__' : 'network_packet_pb2'
  # @@protoc_insertion_point(class_scope:optilab.optnet.NetworkProtoPacketPayload)
  })
_sym_db.RegisterMessage(NetworkProtoPacketPayload)

NetworkProtoPacket = _reflection.GeneratedProtocolMessageType('NetworkProtoPacket', (_message.Message,), {
  'DESCRIPTOR' : _NETWORKPROTOPACKET,
  '__module__' : 'network_packet_pb2'
  # @@protoc_insertion_point(class_scope:optilab.optnet.NetworkProtoPacket)
  })
_sym_db.RegisterMessage(NetworkProtoPacket)

PointToPointProtoPacket = _reflection.GeneratedProtocolMessageType('PointToPointProtoPacket', (_message.Message,), {
  'DESCRIPTOR' : _POINTTOPOINTPROTOPACKET,
  '__module__' : 'network_packet_pb2'
  # @@protoc_insertion_point(class_scope:optilab.optnet.PointToPointProtoPacket)
  })
_sym_db.RegisterMessage(PointToPointProtoPacket)

BroadcastProtoPacket = _reflection.GeneratedProtocolMessageType('BroadcastProtoPacket', (_message.Message,), {

  'ProtoNetworkAddress' : _reflection.GeneratedProtocolMessageType('ProtoNetworkAddress', (_message.Message,), {
    'DESCRIPTOR' : _BROADCASTPROTOPACKET_PROTONETWORKADDRESS,
    '__module__' : 'network_packet_pb2'
    # @@protoc_insertion_point(class_scope:optilab.optnet.BroadcastProtoPacket.ProtoNetworkAddress)
    })
  ,

  'NetworkMapEntry' : _reflection.GeneratedProtocolMessageType('NetworkMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _BROADCASTPROTOPACKET_NETWORKMAPENTRY,
    '__module__' : 'network_packet_pb2'
    # @@protoc_insertion_point(class_scope:optilab.optnet.BroadcastProtoPacket.NetworkMapEntry)
    })
  ,
  'DESCRIPTOR' : _BROADCASTPROTOPACKET,
  '__module__' : 'network_packet_pb2'
  # @@protoc_insertion_point(class_scope:optilab.optnet.BroadcastProtoPacket)
  })
_sym_db.RegisterMessage(BroadcastProtoPacket)
_sym_db.RegisterMessage(BroadcastProtoPacket.ProtoNetworkAddress)
_sym_db.RegisterMessage(BroadcastProtoPacket.NetworkMapEntry)


_BROADCASTPROTOPACKET_NETWORKMAPENTRY._options = None
# @@protoc_insertion_point(module_scope)
