from os import getenv
from pathlib import Path

class Config:
    def __init__(self):
        self.fst_dir = getenv("FST_DIR", "/fst_models")
        self.console_log_level = getenv("CONSOLE_LOG_LEVEL", "DEBUG")
        self.file_log_level = getenv("FILE_LOG_LEVEL", "DEBUG")
        self.file_log_dir = getenv("FILE_LOG_DIR", str(Path().absolute() / "logs"))