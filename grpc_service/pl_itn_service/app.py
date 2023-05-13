from argparse import ArgumentParser
from concurrent import futures
from signal import signal, SIGTERM, SIGINT
from os import getenv
from pathlib import Path

import grpc

from pl_itn_service.proto import api_pb2_grpc
from pl_itn_service.service import PlItnService
from pl_itn_service.logger import Logger


def parser():
    parser = ArgumentParser(allow_abbrev=False)

    parser.add_argument(
        "--fst-dir",
        dest="fst_dir",
        default=getenv("FST_DIR", "/fst_models"),
        help="Directory that contains fst models.",
        type=str,
    )
    parser.add_argument(
        "--console-log-level",
        dest="console_log_level",
        default=getenv("CONSOLE_LOG_LEVEL", "DEBUG"),
        help="Console logging level.",
        type=str,
    )
    parser.add_argument(
        "--file-log-level",
        dest="file_log_level",
        default=getenv("FILE_LOG_LEVEL", "INFO"),
        help="File logging level.",
        type=str,
    )
    parser.add_argument(
        "--file-log-dir",
        dest="file_log_dir",
        default=getenv("FILE_LOG_DIR", str(Path().absolute() / "logs")),
        help="A directory for logs storage.",
        type=str,
    )

    return parser.parse_args()


class Server:
    @staticmethod
    def run(args, port: int = 10010, max_workers: int = 10):
        logger = Logger(
            name=__name__,
            console_log_level=args.console_log_level,
            file_log_level=args.file_log_level,
            file_log_dir=args.file_log_dir,
        ).logger
        logger.info(f"Starting pl_itn grpc service on port {port}...")
        try:
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
            api_pb2_grpc.add_PlItnServicer_to_server(PlItnService(args), server)

        except Exception as e:
            logger.error(e)
            raise e

        server.add_insecure_port(f"[::]:{port}")
        server.start()

        def handle_sig(*_):
            logger.info("Shutting down gracefully.")
            done_event = server.stop(30)
            done_event.wait(30)
            logger.info("Done.")

        signal(SIGTERM, handle_sig)
        signal(SIGINT, handle_sig)

        server.wait_for_termination()


def main():
    args = parser()
    Server.run(args)


if __name__ == "__main__":
    main()
