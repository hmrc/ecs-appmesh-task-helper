import asyncio
import logging
import sys
from envoy_manager import EnvoyManager
from environment_variables import EnvironmentVariables

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


async def sigterm_handler(loop):
    LOGGER.info('{ "message": "SIGTERM received" }')
    environment_variables = EnvironmentVariables()
    await asyncio.sleep(environment_variables.get_drain_delay())
    envoy_manager = EnvoyManager()
    envoy_manager.healthcheck_fail()
    await asyncio.sleep(environment_variables.get_drain_timeout())
    loop.stop()


loop = asyncio.get_event_loop()


loop.add_signal_handler(15, lambda: asyncio.ensure_future(sigterm_handler(loop)))

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()

LOGGER.info('{ "message": "Exiting the process" }')

sys.exit(0)
