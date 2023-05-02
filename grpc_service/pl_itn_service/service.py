from pathlib import Path

from grpc import StatusCode

from google.protobuf import any_pb2
from google.rpc import code_pb2
from google.rpc import error_details_pb2
from google.rpc import status_pb2

from grpc_status import rpc_status

from pl_itn_service.grammar_loader import GrammarLoader, GrammarLoaderError
from pl_itn_service.logger import Logger
from pl_itn_service.proto import api_pb2, api_pb2_grpc

from pl_itn import Normalizer, Grammar, GrammarType


class PlItnService(api_pb2_grpc.PlItnServicer):
    def __init__(self, args):
        self.logger = Logger(
            name="gRPC pl_itn_logger",
            console_log_level=args.console_log_level,
            file_log_level=args.file_log_level,
            file_log_dir=args.file_log_dir,
        ).logger

        self.grammar_loader = GrammarLoader(Path(args.fst_dir))
        self.normalizer = Normalizer()
        self.logger.info("gRPC pl_itn_servicer initialized.")

    def Normalize(self, request, context):
        text = request.text
        tagger = request.tagger if request.HasField("tagger") else None
        verbalizer = request.verbalizer if request.HasField("verbalizer") else None
        try:
            self.logger.debug(f"Normalizing text: {text}")
            if tagger is None and verbalizer is None:
                normalized_text = self.normalizer(text)
            else:
                self.logger.debug(
                    f"Alernative grammar requested, creating temporary Normalizer instance..."
                )
                normalizer_kwargs = {}
                if tagger:
                    self.logger.debug(f"tagger: {tagger.name}")
                    (
                        tagger_path,
                        tagger_description,
                    ) = self.grammar_loader.get_specified_fst(
                        tagger.name, GrammarType.TAGGER
                    )
                    normalizer_kwargs["tagger_fst_path"] = tagger_path
                if verbalizer:
                    self.logger.debug(f"verbalizer: {verbalizer.name}")
                    (
                        verbalizer_path,
                        verbalizer_description,
                    ) = self.grammar_loader.get_specified_fst(
                        verbalizer.name, GrammarType.VERBALIZER
                    )
                    normalizer_kwargs["verbalizer_fst_path"] = verbalizer_path

                temp_normalizer = Normalizer(**normalizer_kwargs)
                normalized_text = temp_normalizer(text)

            return api_pb2.NormalizeResponse(normalized_text=normalized_text)

        except GrammarLoaderError as e:
            self.logger.error(e.message)
            context.set_code(e.grpc_error)
            context.set_details(e.message)
        except Exception as e:
            self.logger.error(e)
            context.set_code(StatusCode.UNKNOWN)
            context.set_details(f"Unknown error ocurred: {e}")
        return api_pb2.NormalizeResponse()

    def GetNormalizerSettings(self, request, context):
        try:
            tagger = self._grammar_to_fst_details(self.normalizer.tagger)
            verbalizer = self._grammar_to_fst_details(self.normalizer.verbalizer)
            return api_pb2.NormalizerSettings(tagger=tagger, verbalizer=verbalizer)

        except Exception as e:
            self.logger.error(e)
            context.set_code(StatusCode.UNKNOWN)
            context.set_details(f"Unknown error ocurred: {e}")
            return api_pb2.NormalizerSettings()

    def _grammar_to_fst_details(self, grammar: Grammar):
        return api_pb2.FstDetails(
            name=grammar.fst_path.name,
            type=api_pb2.FstType.Value(grammar.grammar_type.name),
            description=grammar.description,
        )

    def ListTaggerFst(self, request, context):
        try:
            available_taggers = self.grammar_loader.get_available_fst(
                GrammarType.TAGGER
            )
            list_taggers_response = [
                api_pb2.FstDetails(
                    name=fst_name,
                    type=api_pb2.FstType.TAGGER,
                    description=fst_desctiption,
                )
                for (fst_name, fst_desctiption) in available_taggers.items()
            ]
            return api_pb2.ServiceInfoResponse(fst=list_taggers_response)

        except GrammarLoaderError as e:
            self.logger.error(e.message)
            context.set_code(e.grpc_error)
            context.set_details(e.message)
        except Exception as e:
            self.logger.error(e)
            context.set_code(StatusCode.UNKNOWN)
            context.set_details(f"Unknown error ocurred: {e}")

        return api_pb2.ServiceInfoResponse()

    def ListVerbalizerFst(self, request, context):
        try:
            available_verbalizers = self.grammar_loader.get_available_fst(
                GrammarType.VERBALIZER
            )
            list_verbalizers_response = [
                api_pb2.FstDetails(
                    name=fst_name,
                    type=api_pb2.FstType.VERBALIZER,
                    description=fst_desctiption,
                )
                for (fst_name, fst_desctiption) in available_verbalizers.items()
            ]
            return api_pb2.ServiceInfoResponse(fst=list_verbalizers_response)

        except GrammarLoaderError as e:
            self.logger.error(e.message)
            context.set_code(e.grpc_error)
            context.set_details(e.message)
        except Exception as e:
            self.logger.error(e)
            context.set_code(StatusCode.UNKNOWN)
            context.set_details(f"Unknown error ocurred: {e}")

        return api_pb2.ServiceInfoResponse()

    def SetFst(self, request, context):
        fst_name = request.name
        fst_type = request.type
        try:
            grammar_type = GrammarType[api_pb2.FstType.Name(fst_type)]
            fst_path, description = self.grammar_loader.get_specified_fst(
                fst_name, grammar_type
            )

            self.normalizer.set_grammar(fst_path, grammar_type, description)

        except GrammarLoaderError as e:
            self.logger.error(e.message)
            context.set_code(e.grpc_error)
            context.set_details(e.message)
        except Exception as e:
            self.logger.error(e)
            context.set_code(StatusCode.UNKNOWN)
            context.set_details(f"Unknown error ocurred: {e}")
            ...
        return api_pb2.SetFstResponse()
