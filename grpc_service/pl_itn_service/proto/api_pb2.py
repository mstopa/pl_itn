# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pl_itn_service/proto/api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1epl_itn_service/proto/api.proto\x12\tpl_itn.v1"\x96\x01\n\x10NormalizeRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12*\n\x06tagger\x18\x02 \x01(\x0b\x32\x15.pl_itn.v1.FstDetailsH\x00\x88\x01\x01\x12.\n\nverbalizer\x18\x03 \x01(\x0b\x32\x15.pl_itn.v1.FstDetailsH\x01\x88\x01\x01\x42\t\n\x07_taggerB\r\n\x0b_verbalizer",\n\x11NormalizeResponse\x12\x17\n\x0fnormalized_text\x18\x01 \x01(\t"\x14\n\x12ServiceInfoRequest"9\n\x13ServiceInfoResponse\x12"\n\x03\x66st\x18\x01 \x03(\x0b\x32\x15.pl_itn.v1.FstDetails"f\n\x12NormalizerSettings\x12%\n\x06tagger\x18\x01 \x01(\x0b\x32\x15.pl_itn.v1.FstDetails\x12)\n\nverbalizer\x18\x02 \x01(\x0b\x32\x15.pl_itn.v1.FstDetails"f\n\nFstDetails\x12\x0c\n\x04name\x18\x01 \x01(\t\x12 \n\x04type\x18\x02 \x01(\x0e\x32\x12.pl_itn.v1.FstType\x12\x18\n\x0b\x64\x65scription\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_description"?\n\rSetFstRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12 \n\x04type\x18\x02 \x01(\x0e\x32\x12.pl_itn.v1.FstType"\x10\n\x0eSetFstResponse*%\n\x07\x46stType\x12\n\n\x06TAGGER\x10\x00\x12\x0e\n\nVERBALIZER\x10\x01\x32\x89\x03\n\x05PlItn\x12\x46\n\tNormalize\x12\x1b.pl_itn.v1.NormalizeRequest\x1a\x1c.pl_itn.v1.NormalizeResponse\x12U\n\x15GetNormalizerSettings\x12\x1d.pl_itn.v1.ServiceInfoRequest\x1a\x1d.pl_itn.v1.NormalizerSettings\x12N\n\rListTaggerFst\x12\x1d.pl_itn.v1.ServiceInfoRequest\x1a\x1e.pl_itn.v1.ServiceInfoResponse\x12R\n\x11ListVerbalizerFst\x12\x1d.pl_itn.v1.ServiceInfoRequest\x1a\x1e.pl_itn.v1.ServiceInfoResponse\x12=\n\x06SetFst\x12\x18.pl_itn.v1.SetFstRequest\x1a\x19.pl_itn.v1.SetFstResponseb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "pl_itn_service.proto.api_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _FSTTYPE._serialized_start = 616
    _FSTTYPE._serialized_end = 653
    _NORMALIZEREQUEST._serialized_start = 46
    _NORMALIZEREQUEST._serialized_end = 196
    _NORMALIZERESPONSE._serialized_start = 198
    _NORMALIZERESPONSE._serialized_end = 242
    _SERVICEINFOREQUEST._serialized_start = 244
    _SERVICEINFOREQUEST._serialized_end = 264
    _SERVICEINFORESPONSE._serialized_start = 266
    _SERVICEINFORESPONSE._serialized_end = 323
    _NORMALIZERSETTINGS._serialized_start = 325
    _NORMALIZERSETTINGS._serialized_end = 427
    _FSTDETAILS._serialized_start = 429
    _FSTDETAILS._serialized_end = 531
    _SETFSTREQUEST._serialized_start = 533
    _SETFSTREQUEST._serialized_end = 596
    _SETFSTRESPONSE._serialized_start = 598
    _SETFSTRESPONSE._serialized_end = 614
    _PLITN._serialized_start = 656
    _PLITN._serialized_end = 1049
# @@protoc_insertion_point(module_scope)