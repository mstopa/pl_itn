import pytest

def pytest_addoption(parser, autouse=True):
    parser.addoption("--save-results", action="store_true", help="Save test results.")

@pytest.fixture(scope='session', autouse=True)
def save_results(request):
    return request.config.getoption("--save-results")
