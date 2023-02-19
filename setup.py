import ast
from pathlib import Path
import re
from setuptools import setup, find_packages

project_root = Path(__file__).parent

install_requires = [
    "pynini>=2.1.4",
    "pyyaml>=6.0"
]

with (Path(__file__).parent / "pl_itn/VERSION.py").open() as f:
    version = ast.literal_eval(re.search("^__version__ = (.+?)$", f.read(), re.M).group(1))

setup(
    name="pl_itn",
    version=version,
    description="FST Inverse Text Normalization system",
    long_description=(project_root / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/mstopa/pl_itn",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={"console_scripts": ["pl_itn = pl_itn.__main__:main"]},
)
