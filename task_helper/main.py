import asyncio
import logging
import os
import sys
from envoy_manager import EnvoyManager

LOGGER = logging.getLogger(__name__)


async def sigterm_handler(loop):
    LOGGER.info("SIGTERM received")
    envoy_manager = EnvoyManager()
    envoy_manager.healthcheck_fail()
    await asyncio.sleep(os.getenv("DRAIN_TIMEOUT", default=40))
    loop.stop()


loop = asyncio.get_event_loop()


loop.add_signal_handler(15, lambda: asyncio.ensure_future(sigterm_handler(loop)))

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()

LOGGER.info("Exiting the process")

sys.exit(0)
