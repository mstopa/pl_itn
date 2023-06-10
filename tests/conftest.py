from pathlib import Path

import pytest

def pytest_addoption(parser):
    parser.addoption("--config", type=Path, required=True, help="Path to config file.")
    parser.addoption("--grammars", type=Path, default=Path("pl_itn/grammars"), help="Path grammars directory.")

@pytest.fixture()
def config_path(pytestconfig):
    return Path(pytestconfig.getoption("--config"))

@pytest.fixture()
def grammars_dir(pytestconfig):
    return Path(pytestconfig.getoption("--grammars"))