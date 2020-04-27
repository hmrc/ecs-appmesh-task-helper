import pytest
import requests
from unittest import mock

from envoy_manager import EnvoyManager


def test_healthcheck_fail(caplog):
    envoy_manager = EnvoyManager()
    with mock.patch("envoy_manager.requests.post") as mock_post:
        mock_post.return_value = "OK"
        assert envoy_manager.healthcheck_fail() is True
