import requests
import logging

LOGGER = logging.getLogger(__name__)


class EnvoyManager:
    def __init__(self) -> None:
        return None

    def healthcheck_fail(self):
        LOGGER.info("Signalling envoy to fail the task")
        url = "http://127.0.0.1:9901/healthcheck/fail"
        x = requests.post(url)
        return True
