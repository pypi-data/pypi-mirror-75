import logging
import sys
import warnings

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Ignore IBMQ provider warnings
if not sys.warnoptions:
    warnings.filterwarnings(
        "ignore",
        message=r".*qiskit-ibmq-provider.*",
        category=RuntimeWarning)

try:
    # Package nest_asyncio enables the ability to synchronously
    # wait for awaitables using run_until_complete() even in
    # those cases where the loop is already running.
    # This is specially useful in a Jupyter environment to avoid the
    # "RuntimeError: This event loop is already running" errors.
    import nest_asyncio
    nest_asyncio.apply()
    logger.info("Patched loop with %s", nest_asyncio)
except ImportError:
    logger.info((
        "Using the default event loop instead of nest_asyncio. "
        "Please note that you will not be able to use "
        "synchronous methods (e.g. status()) if the "
        "loop is already running (as is the case in Jupyter)."
    ))
