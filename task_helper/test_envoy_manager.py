from unittest import mock

from envoy_manager import EnvoyManager


def test_healthcheck_fail(caplog):
    envoy_manager = EnvoyManager()
    with mock.patch("envoy_manager.requests.post") as mock_post:
        mock_post.return_value = "OK"

        envoy_manager.healthcheck_fail()

        mock_post.assert_called_once()


def test_healthcheck_fail_exception(caplog):
    envoy_manager = EnvoyManager()
    with mock.patch("envoy_manager.requests.post") as mock_post:
        mock_post.side_effect = ConnectionError()

        envoy_manager.healthcheck_fail()

        mock_post.assert_called_once()

        # assert that there's no exceptions raised
