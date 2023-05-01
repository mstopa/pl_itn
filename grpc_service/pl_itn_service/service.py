from pathlib import Path

from grpc import StatusCode

from google.protobuf import any_pb2
from google.rpc import code_pb2
from google.rpc import error_details_pb2
from google.rpc import status_pb2

from grpc_status import rpc_status

from pl_itn_service.logger import Logger
from pl_itn_service.proto import api_pb2, api_pb2_grpc

from pl_itn import Normalizer, Grammar

class PlItnService(api_pb2_grpc.PlItnServicer):
    def __init__(self, args):
        self.logger = Logger(
            name="gRPC pl_itn_logger",
            console_log_level=args.console_log_level,
            file_log_level=args.file_log_level,
            file_log_dir=args.file_log_dir,
        ).logger

        self.normalizer = Normalizer()
        self.logger.info("gRPC pl_itn_servicer initialized.")

    def Normalize(self, request, context):
        text = request.text
        tagger = request.tagger
        verbalizer = request.verbalizer
        
        try:
            self.logger.debug(f"Normalizing text: {text}")
            normalized_text = self.normalizer.normalize(text)
            return api_pb2.NormalizeResponse(normalized_text=normalized_text)

        except Exception as e:
            self.logger.error(e)
            context.set_code(StatusCode.UNKNOWN)
            context.set_details(f"Unknown error ocurred: {e}")
            return api_pb2.NormalizeResponse()
        
    
    def GetNormalizerSettings(self, request, context):

        try:
            tagger = self._grammar_to_fst_details(self.normalizer.tagger)
            verbalizer = self._grammar_to_fst_details(self.normalizer.verbalizer)
            return api_pb2.NormalizerSettings(
                tagger=tagger,
                verbalizer=verbalizer
            )

        except Exception as e:
            self.logger.error(e)
            context.set_code(StatusCode.UNKNOWN)
            context.set_details(f"Unknown error ocurred: {e}")
            return api_pb2.NormalizerSettings()



    def _grammar_to_fst_details(self, grammar: Grammar):
        return api_pb2.FstDetails(
            name = grammar.fst_path.name,
            type = api_pb2.FstType.Value(grammar.grammar_type.name),
            description = grammar.description
        )

    def ListTaggerFst(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListVerbalizerFst(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChangeDefaultFst(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')