import os


class EnvironmentVariables:
    def get_drain_delay(self) -> int:
        return self._get_env_var("DRAIN_DELAY", 40)

    def get_drain_timeout(self) -> int:
        return self._get_env_var("DRAIN_TIMEOUT", 40)

    def _get_env_var(self, name, default) -> int:
        try:
            timeout = int(str(os.getenv(name)))
        except Exception:
            timeout = default
        return timeout
