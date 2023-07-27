from unittest import mock
import requests

from application_health_check import ApplicationHealthCheck


def test_is_healthy_true(caplog):
    application_health_check = ApplicationHealthCheck("8080", "/ping/ping")
    with mock.patch("application_health_check.requests.get") as mock_post:
        mock_post.return_value = "OK"

        assert application_health_check.is_healthy()

        mock_post.assert_called_once()


def test_is_healthy_false(caplog):
    application_health_check = ApplicationHealthCheck("8080", "/ping/ping")
    with mock.patch("application_health_check.requests.get") as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout()

        assert not application_health_check.is_healthy()

        mock_post.assert_called_once()

        # assert that there's no exceptions raised
