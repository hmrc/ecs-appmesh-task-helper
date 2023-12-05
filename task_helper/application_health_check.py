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
            response = requests.get(url, timeout=2.5)
        except requests.exceptions.RequestException as err:
            LOGGER.info(f"Service instance not healthy: {err}")
            return False
        return True
