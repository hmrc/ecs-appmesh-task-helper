import pytest
from unittest import mock

from environment_variables import EnvironmentVariables


@pytest.fixture
def environ(monkeypatch):
    # contains all the required environment variables.
    data = {
        "FOO": "60",
    }
    for var_name, var_value in data.items():
        monkeypatch.setenv(var_name, var_value)


@pytest.fixture
def environ_bad(monkeypatch):
    # contains all the required environment variables.
    data = {
        "FOO": "BAR",
    }
    for var_name, var_value in data.items():
        monkeypatch.setenv(var_name, var_value)


def test_get_drain_delay_without_environment():
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_delay() == 40


def test_get_drain_timeout_without_environment():
    environment_variables = EnvironmentVariables()
    assert environment_variables.get_drain_timeout() == 40


@pytest.mark.usefixtures("environ")
def test__get_env_var_with_environment():
    environment_variables = EnvironmentVariables()
    assert environment_variables._get_integer_env_var("FOO", 40) == 60


@pytest.mark.usefixtures("environ_bad")
def test_get_drain_delay_with_bad_environment():
    environment_variables = EnvironmentVariables()
    assert environment_variables._get_integer_env_var("FOO", 40) == 40
