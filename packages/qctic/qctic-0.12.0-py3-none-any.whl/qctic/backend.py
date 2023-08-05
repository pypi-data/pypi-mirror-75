import asyncio
import copy
import logging
import uuid

from qiskit.providers import BaseBackend
from qiskit.providers.aer.backends import (QasmSimulator, StatevectorSimulator,
                                           UnitarySimulator)
from qiskit.providers.models import BackendStatus, QasmBackendConfiguration
from qiskit.qobj import QasmQobj as Qobj

from qctic.__version__ import __version__
from qctic.job import QCticJob

_logger = logging.getLogger(__name__)


class BaseQCticSimulator(BaseBackend):
    """Base class for CTIC Erwin simulator backends."""

    N_QUBITS = 32
    MAX_EXPERIMENTS = 20

    BASE_DESCRIPTION = (
        "A remote quantum simulator based on "
        "Aer's {} that runs on the "
        "high-performance CTIC Erwin computer"
    )

    BASE_CONFIGURATION = {
        "backend_version": __version__,
        "n_qubits": N_QUBITS,
        "url": "https://bitbucket.org/fundacionctic/erwin-qiskit",
        "local": False,
        "max_experiments": MAX_EXPERIMENTS
    }

    def __init__(self, *args, **kwargs):
        """Constructor."""

        kwargs["configuration"] = self.default_configuration()
        super().__init__(*args, **kwargs)

    @classmethod
    def default_configuration(cls):
        """dict: Default base configuration for this backend class."""

        raise NotImplementedError

    @property
    def api(self):
        """QCticAPI: The API instance of this backend's provider."""

        return self.provider().api

    def _res_to_job(self, res):
        return QCticJob(self, res["job_id"], Qobj.from_dict(res["qobj"]), remote_job=res)

    def _default_backend_status(self):
        return BackendStatus(
            backend_name=self.name(),
            backend_version=self.configuration().backend_version,
            operational=False,
            pending_jobs=0,
            status_msg="The Erwin quantum simulation platform is not currently operational")

    def _res_to_backend_status(self, res):
        return BackendStatus(
            backend_name=self.name(),
            backend_version=self.configuration().backend_version,
            operational=res.get("operational"),
            pending_jobs=res.get("pending_jobs"),
            status_msg="The Erwin quantum simulation platform is operational")

    def _log_status_ex(self, ex):
        _logger.warning("Error fetching status: {}".format(ex))

    def run(self, qobj, **kwargs):
        """Run a qobj on the backend.

        Args:
            qobj (Qobj): The Qobj to be executed.

        Returns:
            QCticJob: The simulation job.

        Additional Information:
            * The ``kwargs`` will be passed to the ``run`` method of the 
              ``AerBackend`` instance in the remote simulation platform.
        """

        is_async = bool(kwargs.pop("async_submit", False))

        job_id = str(uuid.uuid4())
        job = QCticJob(self, job_id, qobj, run_params=kwargs)

        if is_async:
            _logger.debug("Asynchronous job submit: %s", job_id)
            job.submit_task = asyncio.ensure_future(job.submit_async())
        else:
            _logger.debug("Synchronous job submit: %s", job_id)
            job.submit()

        return job

    def status(self):
        """Fetch the current status of the simulation platform.

        Returns:
            BackendStatus: The status.
        """

        try:
            res = self.api.get_backend_status_sync()
            return self._res_to_backend_status(res)
        except Exception as ex:
            self._log_status_ex(ex)
            return self._default_backend_status()

    def jobs(self, **kwargs):
        """Fetch a set of jobs that match the given filters.

        The filters can be passed as optional keyword arguments 
        that match those of the ``QCticAPI.get_jobs`` method.

        Returns:
            list(QCticJob): List of jobs.
        """

        res = self.api.get_jobs_sync(**kwargs)
        return [self._res_to_job(item) for item in res]

    def retrieve_job(self, job_id):
        """Fetch a job given its ID.

        Args:
            job_id (str): Job ID.

        Returns:
            QCticJob: The job.
        """

        job_res = self.api.get_job_sync(job_id)
        return self._res_to_job(job_res)

    async def status_async(self):
        """Asynchronous version of the ``status`` method."""

        try:
            res = await self.api.get_backend_status()
            return self._res_to_backend_status(res)
        except Exception as ex:
            self._log_status_ex(ex)
            return self._default_backend_status()

    async def jobs_async(self, **kwargs):
        """Asynchronous version of the ``jobs`` method."""

        res = await self.api.get_jobs(**kwargs)
        return [self._res_to_job(item) for item in res]

    async def retrieve_job_async(self, job_id):
        """Asynchronous version of the ``retrieve_job`` method."""

        res = await self.api.get_job(job_id)
        return self._res_to_job(res)


class QCticQasmSimulator(BaseQCticSimulator):
    """Backend that represents the CTIC Erwin simulation platform.

    Remote jobs are executed on Aer's QasmSimulator."""

    NAME = "ctic_erwin_qasm_simulator"

    @classmethod
    def default_configuration(cls):
        """Returns the default configuration for the Erwin QasmSimulator.

        Returns:
            QasmBackendConfiguration: The configuration object.
        """

        conf = copy.deepcopy(QasmSimulator.DEFAULT_CONFIGURATION)
        conf.update(cls.BASE_CONFIGURATION)

        conf.update({
            "backend_name": cls.NAME,
            "description": cls.BASE_DESCRIPTION.format("QasmSimulator")
        })

        return QasmBackendConfiguration.from_dict(conf)


class QCticStatevectorSimulator(BaseQCticSimulator):
    """Backend that represents the CTIC Erwin simulation platform.

    Remote jobs are executed on Aer's StatevectorSimulator."""

    NAME = "ctic_erwin_statevector_simulator"

    @classmethod
    def default_configuration(cls):
        """Returns the default configuration for the Erwin StatevectorSimulator.

        Returns:
            QasmBackendConfiguration: The configuration object.
        """

        conf = copy.deepcopy(StatevectorSimulator.DEFAULT_CONFIGURATION)
        conf.update(cls.BASE_CONFIGURATION)

        conf.update({
            "backend_name": cls.NAME,
            "description": cls.BASE_DESCRIPTION.format("StatevectorSimulator")
        })

        return QasmBackendConfiguration.from_dict(conf)


class QCticUnitarySimulator(BaseQCticSimulator):
    """Backend that represents the CTIC Erwin simulation platform.

    Remote jobs are executed on Aer's UnitarySimulator."""

    NAME = "ctic_erwin_unitary_simulator"

    @classmethod
    def default_configuration(cls):
        """Returns the default configuration for the Erwin UnitarySimulator.

        Returns:
            QasmBackendConfiguration: The configuration object.
        """

        conf = copy.deepcopy(UnitarySimulator.DEFAULT_CONFIGURATION)
        conf.update(cls.BASE_CONFIGURATION)

        conf.update({
            "backend_name": cls.NAME,
            "description": cls.BASE_DESCRIPTION.format("UnitarySimulator")
        })

        return QasmBackendConfiguration.from_dict(conf)
