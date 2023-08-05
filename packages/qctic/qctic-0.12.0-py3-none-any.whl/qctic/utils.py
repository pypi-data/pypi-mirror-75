import asyncio
import time

_BASE_SLEEP = 1.0
_MAX_SLEEP = 30.0
_SLEEP_GROWTH = 1.2
_TIMEOUT = None


class QcticResultTimeoutError(Exception):
    pass


def _raise_if_timeout(start, timeout):
    if timeout is None:
        return

    diff = time.time() - start

    if diff >= timeout:
        raise QcticResultTimeoutError(
            "Timeout exceeded ({} secs)".format(timeout))


def wait_result(
        job, base_sleep=_BASE_SLEEP, max_sleep=_MAX_SLEEP,
        sleep_growth=_SLEEP_GROWTH, timeout=_TIMEOUT):
    sleep = base_sleep
    start = time.time()

    while True:
        res = job.result(fetch=True)

        if res:
            return res

        _raise_if_timeout(start, timeout)
        time.sleep(sleep)
        sleep = min(sleep * sleep_growth, max_sleep)


async def wait_result_async(
        job, base_sleep=_BASE_SLEEP, max_sleep=_MAX_SLEEP,
        sleep_growth=_SLEEP_GROWTH, timeout=_TIMEOUT):
    sleep = base_sleep
    start = time.time()

    while True:
        res = await job.result_async(fetch=True)

        if res:
            return res

        _raise_if_timeout(start, timeout)
        await asyncio.sleep(sleep)
        sleep = min(sleep * sleep_growth, max_sleep)
