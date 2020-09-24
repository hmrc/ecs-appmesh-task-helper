import asyncio
import logging
import sys

from envoy_manager import EnvoyManager
from environment_variables import EnvironmentVariables

from pythonjsonlogger import jsonlogger

LOGGER = logging.getLogger()

logHandler = logging.StreamHandler(sys.stdout)
format_str = "%(message)%(levelname)%(name)%(asctime)"
logHandler.setFormatter(jsonlogger.JsonFormatter(format_str))
LOGGER.addHandler(logHandler)
LOGGER.setLevel(logging.INFO)


async def sigterm_handler(loop):
    environment_variables = EnvironmentVariables()
    drain_delay = environment_variables.get_drain_delay()
    drain_timeout = environment_variables.get_drain_timeout()

    # This first delay is to allow new tasks to get up and running before killing the existing tasks
    LOGGER.info(f"SIGTERM received, waiting for {drain_delay} seconds")
    await asyncio.sleep(drain_delay)

    # Send the command to Envoy that effectively stops traffic going to the app
    envoy_manager = EnvoyManager()
    envoy_manager.healthcheck_fail()

    # Now allow existing requests to complete gracefully
    LOGGER.info(f"Waiting for {drain_timeout} seconds to allow for draining to finish")
    await asyncio.sleep(drain_timeout)

    # Stopping the task here causes the cascading termination process which is based on the container dependencies
    loop.stop()


loop = asyncio.get_event_loop()


loop.add_signal_handler(15, lambda: asyncio.ensure_future(sigterm_handler(loop)))

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()
