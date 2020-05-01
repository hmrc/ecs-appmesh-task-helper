import pytest
from unittest import mock

from environment_variables import EnvironmentVariables


@pytest.fixture
def environ(monkeypatch):
    # contains all the required environment variables.
    data = {
        "DRAIN_DELAY": "60",
        "DRAIN_TIMEOUT": "70",
    }
    for var_name, var_value in data.items():
        monkeypatch.setenv(var_name, var_value)


@pytest.fixture
def environ_bad(monkeypatch):
    # contains all the required environment variables.
    data = {
        "DRAIN_DELAY": "FOO",
        "DRAIN_TIMEOUT": "BAR",
    }
    for var_name, var_value in data.items():
        monkeypatch.setenv(var_name, var_value)


def test_get_drain_delay_without_environment(caplog):
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_delay() == 40


def test_get_drain_timeout_without_environment(caplog):
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_timeout() == 40


@pytest.mark.usefixtures("environ")
def test_get_drain_delay_with_environment(caplog):
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_delay() == 60


@pytest.mark.usefixtures("environ")
def test_get_drain_timeout_with_environment(caplog):
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_timeout() == 70


@pytest.mark.usefixtures("environ_bad")
def test_get_drain_delay_with_bad_environment(caplog):
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_delay() == 40


@pytest.mark.usefixtures("environ_bad")
def test_get_drain_timeout_with_bad_environment(caplog):
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_timeout() == 40
