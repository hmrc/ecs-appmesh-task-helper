import requests
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class EnvoyManager:
    def healthcheck_fail(self) -> bool:
        LOGGER.info("Signalling envoy to fail the task")
        url = "http://127.0.0.1:9901/healthcheck/fail"
        try:
            x = requests.post(url)
        except Exception:
            LOGGER.error("An error occurred POSTing to the envoy admin api")
        return True
