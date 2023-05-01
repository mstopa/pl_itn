from pathlib import Path
import re
import ast
from setuptools import setup, find_packages

from pl_itn_service.version import __version__ as package_version

project_root = Path(__file__).parent

setup(
    name="pl_itn_grpc_service",
    version=package_version,
    description="FST Inverse Text Normalization gRPC service",
    url="https://github.com/mstopa/pl_itn",
    packages=find_packages(),
    install_requires=[
        "wheel",
        "pl_itn",
        "grpcio>=1.48.0",
        "grpcio-status>=1.48.0",
        "protobuf>=4.21.0",
    ],
    setup_requires=["wheel"],
    entry_points={"console_scripts": ["pl_itn_service = pl_itn_service.app:main"]},
)