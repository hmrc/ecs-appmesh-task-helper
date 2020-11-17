import os


class EnvironmentVariables:
    def get_drain_delay(self) -> int:
        return self._get_integer_env_var("DRAIN_DELAY", 1)

    def get_drain_timeout(self) -> int:
        return self._get_integer_env_var("DRAIN_TIMEOUT", 10)

    def _get_integer_env_var(self, name, default) -> int:
        try:
            return int(str(os.getenv(name)))
        except Exception:
            return default
