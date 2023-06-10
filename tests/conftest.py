from pathlib import Path

import pytest

def pytest_addoption(parser):
    parser.addoption("--config", type=Path, required=True, help="Path to config file.")

@pytest.fixture()
def config_path(pytestconfig):
    return Path(pytestconfig.getoption("--config"))