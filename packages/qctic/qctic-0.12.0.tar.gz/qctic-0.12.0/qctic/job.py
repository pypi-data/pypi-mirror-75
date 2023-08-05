import asyncio
import collections
import logging
import os
import pprint
import random
import time
import warnings
from functools import wraps

from qiskit.providers import BaseJob, JobError, JobStatus
from qiskit.result import Result

from qctic.utils import wait_result, wait_result_async

_PARAM_TIMEOUT = "timeout"
_PARAM_WAIT = "wait"
_ENV_SIM_RATIO = "QCTIC_SIMULATION_RATIO_WARNING"

_logger = logging.getLogger(__name__)


def _fetch_job_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        fetch = kwargs.pop("fetch", False)

        if not args[0]._remote_job or fetch:
            args[0].fetch_remote()

        return func(*args, **kwargs)

    return wrapper


def _fetch_job_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        fetch = kwargs.pop("fetch", False)

        if not args[0]._remote_job or fetch:
            await args[0].fetch_remote_async()

        return await func(*args, **kwargs)

    return wrapper


async def _dummy_submit_task():
    warn_msg = (
        "Awaiting on undefined submit task: "
        "Pass async_submit=True to run() or execute() to submit jobs asynchronously"
    )

    warnings.warn(warn_msg, UserWarning)

WaitResultParams = collections.namedtuple(
    "WaitResultParams",
    ["timeout", "wait"])


class SimulationRatioWarning(Warning):
    """Warning raised when the simulation ratio of any given job is too low. 
    This usually means that it would be more optimal for the experiments to be executed 
    locally to avoid paying the cost of network latencies and worker initialization."""


class QCticJob(BaseJob):
    """A Qiskit job that is executed remotely in the CTIC Erwin simulation platform."""

    def __init__(self, backend, job_id, qobj, run_params=None, remote_job=None):
        """Constructor.

        Args:
            backend (QCticQasmSimulator): Backend that contains this job.
            job_id (str): ID of the job.
            qobj (Qobj): Qobj that contains the experiment.
            run_params (dict): Optional dict of arbitrary arguments passed
                to the ``run`` method in the remote simulation platform.
        """

        super().__init__(backend, job_id)
        self._qobj = qobj
        self._remote_job = remote_job
        self._fetch_time = None
        self._run_params = run_params
        self._submit_task = None
        self._raised_warning = False

    @property
    def api(self):
        """QCticAPI: The API instance of this job's backend."""

        return self.backend().api

    def qobj(self):
        """Return the Qobj submitted for this job.

        Returns:
            Qobj: The Qobj submitted for this job.
        """

        return self._qobj

    @property
    def run_params(self):
        """dict: Arguments passed to the ``run`` method in the remote simulation platform."""

        return self._run_params

    @property
    def remote_job(self):
        """dict: Serialized version of this job as represented in the remote API."""

        return self._remote_job

    @property
    def time_submit(self):
        """datetime.timedelta: Time spent by the job from submission to the 
        moment it entered the queue. This includes the API network latency."""

        date_submit = self.remote_job.get("date_submit")
        date_queue = self.remote_job.get("date_queue")

        if not date_submit or not date_queue:
            return None

        return date_queue - date_submit

    @property
    def time_enqueued(self):
        """datetime.timedelta: Time spent by the job in the queue waiting to be executed."""

        date_queue = self.remote_job.get("date_queue")
        date_start = self.remote_job.get("date_start")

        if not date_queue or not date_start:
            return None

        return date_start - date_queue

    @property
    def time_running(self):
        """datetime.timedelta: Time spent by the job in an active worker 
        including the environment initialization and simulation."""

        date_start = self.remote_job.get("date_start")
        date_end = self.remote_job.get("date_end")

        if not date_start or not date_end:
            return None

        return date_end - date_start

    @property
    def time_simulation(self):
        """datetime.timedelta: Time spent by the job in the actual simulation."""

        date_ex_start = self.remote_job.get("date_execute_start")
        date_ex_end = self.remote_job.get("date_execute_end")

        if not date_ex_start or not date_ex_end:
            return None

        return date_ex_end - date_ex_start

    @property
    def time_total(self):
        """datetime.timedelta: Total time spent by the job from submission 
        to the moment the final simulation results are persisted."""

        date_submit = self.remote_job.get("date_submit")
        date_end = self.remote_job.get("date_end")

        if not date_submit or not date_end:
            return None

        return date_end - date_submit

    def get_simulation_ratio(self, queue=True):
        """Returns the ratio between the time spent in the actual simulation and the total time 
        including network latency, environment initialization and (optional) queue latency.

        Args:
            queue (bool): (Optional) Take the queue latency into account.

        Returns:
            float: The simulation ratio.
        """

        if not self.time_simulation or not self.time_total:
            return None

        if not queue and not self.time_enqueued:
            return None

        delta_total = self.time_total if queue else self.time_total - self.time_enqueued

        return round(self.time_simulation.total_seconds() / delta_total.total_seconds(), 3)

    @property
    def submit_task(self):
        return self._submit_task if self._submit_task else _dummy_submit_task()

    @submit_task.setter
    def submit_task(self, val):
        if self._submit_task:
            raise ValueError("The submit task has already been defined")

        self._submit_task = val

    def _log_fetch(self):
        _logger.debug("Fetching job: %s", self.job_id())

    def fetch_remote(self):
        self._log_fetch()
        self._remote_job = self.api.get_job_sync(self.job_id())
        self._fetch_time = time.time()

    async def fetch_remote_async(self):
        self._log_fetch()
        self._remote_job = await self.api.get_job(self.job_id())
        self._fetch_time = time.time()

    def _raise_simulation_warning(self):
        limit = os.getenv(_ENV_SIM_RATIO, None)

        if self._raised_warning or limit is None:
            return

        ratio = self.get_simulation_ratio(queue=False)

        if ratio is None:
            return

        try:
            limit = float(limit)
        except Exception as ex:
            _logger.warning("Invalid sim. ratio value (%s): %s", limit, ex)
            return

        if ratio < limit:
            warn_msg = (
                "The simulation time ratio of this job ({}) "
                "appears to be low (<{}). This is without taking "
                "into account wait times in the queue. Please consider "
                "running the simulation locally to optimize wait times."
            ).format(ratio, limit)

            _logger.warning(warn_msg)
            warnings.warn(warn_msg, SimulationRatioWarning)
            self._raised_warning = True

    def _result(self):
        error = self._remote_job.get("error", None)

        if error is not None:
            raise JobError(error)

        result_dict = self._remote_job.get("result", None)
        result = Result.from_dict(result_dict) if result_dict else None

        if result and not result.success:
            status_msg = pprint.pformat([r.status for r in result.results])
            _logger.warning("Some experiments failed:\n%s", status_msg)

        if result and result.success:
            self._raise_simulation_warning()

        return result

    def _status(self):
        return self._remote_job.get("status", None)

    def _get_wait_params(self, *args, **kwargs):
        if _PARAM_TIMEOUT not in kwargs or _PARAM_WAIT not in kwargs:
            return None

        wait = int(kwargs[_PARAM_WAIT])
        timeout = kwargs[_PARAM_TIMEOUT]

        if timeout is not None:
            timeout = int(timeout)

        _logger.debug(
            "Should wait for result (timeout=%s, wait=%s)",
            timeout, wait)

        return WaitResultParams(timeout=timeout, wait=wait)

    @_fetch_job_sync
    def status(self):
        """Return the status of the job, one of the names of the ``JobStatus`` enum.

        Args:
            fetch (bool): (Optional) Fetch the status from the remote API.

        Returns:
            JobStatus: The name of a member of the JobStatus enum.
        """

        return self._status()

    def submit(self):
        """Submit the job to the backend for execution."""

        self.api.post_job_sync(self)

    def cancel(self):
        """Attempt to cancel the job."""

        self.api.cancel_job_sync(self.job_id())

    @_fetch_job_sync
    def result(self, *args, **kwargs):
        """Return the results of the job.

        Args:
            fetch (bool): (Optional) Fetch the result from the remote API.

        Returns:
            Result: The results.

        Raises:
            JobError: If there was an error running the experiment on the remote simulator.
        """

        wait_params = self._get_wait_params(*args, **kwargs)

        if wait_params:
            return wait_result(
                self,
                base_sleep=wait_params.wait,
                timeout=wait_params.timeout,
                sleep_growth=1.0)

        return self._result()

    @_fetch_job_async
    async def status_async(self):
        return self._status()

    async def submit_async(self):
        await self.api.post_job(self)

    async def cancel_async(self):
        await self.api.cancel_job(self.job_id())

    @_fetch_job_async
    async def result_async(self, *args, **kwargs):
        wait_params = self._get_wait_params(*args, **kwargs)

        if wait_params:
            return await wait_result_async(
                self,
                base_sleep=wait_params.wait,
                timeout=wait_params.timeout,
                sleep_growth=1.0)

        return self._result()
