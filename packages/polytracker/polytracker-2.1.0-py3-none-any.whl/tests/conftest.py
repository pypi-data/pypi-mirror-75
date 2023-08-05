import pytest


def pytest_addoption(parser):
    parser.addoption("--json", action="store", default=None, help="Path to JSON file")
    parser.addoption("--forest", action="store", default=None, help="Path to forest file")


@pytest.fixture
def json_path(pytestconfig):
    return pytestconfig.getoption("--json")


@pytest.fixture
def forest_path(pytestconfig):
    return pytestconfig.getoption("--forest")
