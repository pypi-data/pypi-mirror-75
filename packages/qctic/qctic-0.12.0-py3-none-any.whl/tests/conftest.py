import uuid

import pytest

from qctic.api import QCticAPI
from qctic.backend import QCticQasmSimulator
from qctic.job import QCticJob
from qctic.provider import QCticProvider
from tests.utils import fake_qobj


@pytest.fixture(scope="function")
def provider(httpserver):
    api_host = httpserver.url_for("/")
    api = QCticAPI(host=api_host)
    api.auth_token(str(uuid.uuid4()))
    return QCticProvider(api=api)


@pytest.fixture(scope="function")
def job(provider):
    backend = provider.get_backend(QCticQasmSimulator.NAME)
    job_id = str(uuid.uuid4())
    qobj = fake_qobj()
    return QCticJob(backend, job_id, qobj)
