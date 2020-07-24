import requests
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class EnvoyManager:
    def healthcheck_fail(self):
        LOGGER.info("Signalling envoy to fail the task")
        url = "http://127.0.0.1:9901/healthcheck/fail"
        try:
            response = requests.post(url)
            LOGGER.info("Response from {url}: {response.status_code}")
        except Exception:
            LOGGER.exception("An error occurred POSTing to the envoy admin api")
