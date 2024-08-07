import requests
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class ApplicationHealthCheck:
    def __init__(self, port, path):
        self.port = port
        self.path = path

    def is_healthy(self):
        LOGGER.info("Checking the health of the app")
        url = f"http://127.0.0.1:{self.port}{self.path}"
        try:
            response = requests.get(  # noqa: F841
                url, timeout=2.5, allow_redirects=False
            )
        except requests.exceptions.RequestException:
            return False
        return True
