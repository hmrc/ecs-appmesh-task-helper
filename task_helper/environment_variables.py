import os


class EnvironmentVariables:
    def get_drain_delay(self) -> int:
        return self._get_integer_env_var("DRAIN_DELAY", 40)

    def get_drain_timeout(self) -> int:
        return self._get_integer_env_var("DRAIN_TIMEOUT", 80)

    def get_port(self) -> str:
        return self._get_string_env_var("PORT", "8080")

    def get_path(self) -> str:
        return self._get_string_env_var("HEALTHCHECK_PATH", "/ping/ping")

    def _get_integer_env_var(self, name, default) -> int:
        try:
            return int(str(os.getenv(name)))
        except Exception:
            return default

    def _get_string_env_var(self, name, default) -> str:
        if os.getenv(name):
            return str(os.getenv(name))
        else:
            return default
