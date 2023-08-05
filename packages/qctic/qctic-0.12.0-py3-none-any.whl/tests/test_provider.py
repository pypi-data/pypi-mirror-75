import datetime
import json
import os
import random
import uuid

import pytest
from qiskit import Aer, execute
from qiskit.assembler import disassemble
from qiskit.providers import JobStatus
from tests.utils import fake_job_dict, fake_qobj
from werkzeug.wrappers import Response

from qctic.backend import QCticQasmSimulator
from qctic.job import QCticJob
from qctic.provider import QCticProvider

_LOCALHOST = "http://localhost"
_JOB_DICTS = [fake_job_dict() for _ in range(random.randint(1, 10))]
_PENDING_JOBS = random.randint(0, 10)
_JOB_DICT = fake_job_dict()
_STATUS = JobStatus.QUEUED.name


def _clear_api_env():
    env_vars = [
        QCticProvider.ENV_HOST,
        QCticProvider.ENV_USERNAME,
        QCticProvider.ENV_PASSWORD,
        QCticProvider.ENV_TOKEN
    ]

    for item in env_vars:
        os.environ[item] = ""


@pytest.fixture
def clear_env():
    _clear_api_env()
    yield True
    _clear_api_env()


def test_from_env_token(clear_env):
    with pytest.raises(Exception):
        QCticProvider.from_env()

    os.environ[QCticProvider.ENV_HOST] = _LOCALHOST
    os.environ[QCticProvider.ENV_TOKEN] = str(uuid.uuid4())

    assert QCticProvider.from_env()


def test_from_env_basic(clear_env):
    with pytest.raises(Exception):
        QCticProvider.from_env()

    os.environ[QCticProvider.ENV_HOST] = _LOCALHOST
    os.environ[QCticProvider.ENV_USERNAME] = str(uuid.uuid4())

    with pytest.raises(Exception):
        QCticProvider.from_env()

    os.environ[QCticProvider.ENV_PASSWORD] = str(uuid.uuid4())

    assert QCticProvider.from_env()


def test_provider_get_backend(provider):
    all_backends = provider.backends()
    simulator_backends = provider.backends(simulator=True)

    large_backends = provider.backends(
        filters=lambda x: x.configuration().n_qubits >= 10)

    qasm_backend = provider.get_backend(QCticQasmSimulator.NAME)

    assert len(all_backends) > 0
    assert len(simulator_backends) == len(all_backends)
    assert len(large_backends) == len(all_backends)
    assert qasm_backend
    assert qasm_backend in all_backends
    assert qasm_backend in simulator_backends
    assert qasm_backend in large_backends


def test_backend_base_interface(provider):
    backend = provider.get_backend(QCticQasmSimulator.NAME)
    config = backend.configuration()

    assert backend.provider() == provider
    assert backend.name() == QCticQasmSimulator.NAME
    assert backend.status().backend_name == QCticQasmSimulator.NAME
    assert config.backend_name == backend.status().backend_name
    assert config.backend_version
    assert not config.local


def test_backend_run(provider, httpserver):
    arg_key = str(uuid.uuid4())

    def handler(req):
        data = json.loads(req.data)
        assert data["job_id"]
        assert data["run_params"][arg_key]
        return Response()

    httpserver.expect_request("/jobs").respond_with_handler(handler)
    backend = provider.get_backend(QCticQasmSimulator.NAME)
    qobj = fake_qobj()
    job = backend.run(qobj, **{arg_key: True})

    assert job.job_id()
    assert job.api
    assert job.qobj().to_dict() == qobj.to_dict()
    assert job.run_params[arg_key]


@pytest.fixture
def backend_for_status_test(provider, httpserver):
    httpserver.expect_request("/status").respond_with_json({
        "operational": True,
        "pending_jobs": _PENDING_JOBS
    })

    backend = provider.get_backend(QCticQasmSimulator.NAME)

    return backend


def assert_status_test(status):
    assert status.operational
    assert status.pending_jobs == _PENDING_JOBS


def test_backend_status(backend_for_status_test):
    status = backend_for_status_test.status()
    assert_status_test(status)


@pytest.mark.asyncio
async def test_backend_status_async(backend_for_status_test):
    status = await backend_for_status_test.status_async()
    assert_status_test(status)


@pytest.fixture
def backend_for_jobs_test(provider, httpserver):
    def handler(req):
        assert int(req.args["limit"]) == len(_JOB_DICTS)
        return Response(json.dumps(_JOB_DICTS))

    httpserver.expect_request("/jobs").respond_with_handler(handler)
    backend = provider.get_backend(QCticQasmSimulator.NAME)

    return backend


def assert_jobs_test(jobs):
    assert len(jobs) == len(_JOB_DICTS)

    assert all([
        next(True for item in _JOB_DICTS if item["job_id"] == job.job_id())
        for job in jobs
    ])


def test_backend_jobs(backend_for_jobs_test):
    jobs = backend_for_jobs_test.jobs(limit=len(_JOB_DICTS))
    assert_jobs_test(jobs)


@pytest.mark.asyncio
async def test_backend_jobs_async(backend_for_jobs_test):
    jobs = await backend_for_jobs_test.jobs_async(limit=len(_JOB_DICTS))
    assert_jobs_test(jobs)


@pytest.fixture
def backend_for_retrieve_test(provider, httpserver):
    def handler(req):
        return Response(json.dumps(_JOB_DICT))

    url = "/jobs/{}".format(_JOB_DICT["job_id"])
    httpserver.expect_request(url).respond_with_handler(handler)
    backend = provider.get_backend(QCticQasmSimulator.NAME)

    return backend


def test_backend_retrieve_job(backend_for_retrieve_test):
    job_id = _JOB_DICT["job_id"]
    job = backend_for_retrieve_test.retrieve_job(job_id)
    assert job.job_id() == job_id


@pytest.mark.asyncio
async def test_backend_retrieve_job_async(backend_for_retrieve_test):
    job_id = _JOB_DICT["job_id"]
    job = await backend_for_retrieve_test.retrieve_job_async(job_id)
    assert job.job_id() == job_id


def test_job_base_interface(provider):
    backend = provider.get_backend(QCticQasmSimulator.NAME)
    job_id = str(uuid.uuid4())
    qobj = fake_qobj()
    job = QCticJob(backend, job_id, qobj)

    assert job.backend() == backend
    assert job.job_id() == job_id


@pytest.fixture
def job_for_status_test(job, httpserver):
    status = JobStatus.QUEUED.name
    url = "/jobs/{}".format(job.job_id())

    httpserver.expect_request(url).respond_with_json({
        "job_id": job.job_id(),
        "qobj": job.qobj().to_dict(),
        "date_submit": datetime.datetime.now().isoformat(),
        "status": status
    })

    return job


def test_job_status(job_for_status_test):
    assert job_for_status_test.status() == _STATUS


@pytest.mark.asyncio
async def test_job_status_async(job_for_status_test):
    the_status = await job_for_status_test.status_async()
    assert the_status == _STATUS


@pytest.fixture
def job_for_submit_test(job, httpserver):
    def handler(req):
        data = json.loads(req.data)
        assert data["job_id"] == job.job_id()
        assert data["qobj"] == job.qobj().to_dict()
        return Response()

    httpserver.expect_request("/jobs").respond_with_handler(handler)

    return job


def test_job_submit(job_for_submit_test):
    job_for_submit_test.submit()


@pytest.mark.asyncio
async def test_job_submit_async(job_for_submit_test):
    await job_for_submit_test.submit_async()


@pytest.fixture
def job_for_cancel_test(job, httpserver):
    def handler(req):
        data = json.loads(req.data)
        assert data["status"] == JobStatus.CANCELLED.name
        return Response()

    url = "/jobs/{}".format(job.job_id())
    httpserver.expect_request(url).respond_with_handler(handler)

    return job


def test_job_cancel(job_for_cancel_test):
    job_for_cancel_test.cancel()


@pytest.mark.asyncio
async def test_job_cancel_async(job_for_cancel_test):
    await job_for_cancel_test.cancel_async()


def test_job_result(job, httpserver):
    circuits, _run_config, _user_qobj_header = disassemble(job.qobj())
    simulator = Aer.get_backend("qasm_simulator")
    simulator_job = execute(circuits[0], simulator)
    simulator_result = simulator_job.result()
    url = "/jobs/{}".format(job.job_id())
    now = datetime.datetime.now()

    httpserver.expect_request(url).respond_with_json({
        "job_id": job.job_id(),
        "qobj": job.qobj().to_dict(),
        "date_submit": now.isoformat(),
        "date_start": (now + datetime.timedelta(1)).isoformat(),
        "date_end": (now + datetime.timedelta(2)).isoformat(),
        "status": JobStatus.DONE.name,
        "result": simulator_result.to_dict()
    })

    result = job.result()

    assert result.to_dict() == simulator_result.to_dict()


def test_job_fetch_remote(job, httpserver):
    job_dict = {
        "job_id": job.job_id(),
        "qobj": job.qobj().to_dict(),
        "date_submit": datetime.datetime.now().isoformat(),
        "status": JobStatus.INITIALIZING.name
    }

    count = [0]

    def handler(req):
        count[0] += 1
        return Response(json.dumps(job_dict))

    url = "/jobs/{}".format(job.job_id())
    httpserver.expect_request(url).respond_with_handler(handler)

    assert count[0] == 0
    assert job.status() == job_dict["status"]
    assert count[0] == 1
    assert job.status() == job_dict["status"]
    assert count[0] == 1
    assert job.status(fetch=True) == job_dict["status"]
    assert count[0] == 2
