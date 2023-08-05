# pylint: disable=no-member

import asyncio
import datetime
import json
import random
import re
import uuid

import pytest
from qiskit import assemble, execute
from qiskit.providers import JobStatus
from werkzeug.wrappers import Response

from qctic.api import QCticAPI
from qctic.job import QCticJob
from qctic.provider import QCticProvider
from tests.utils import fake_circuit, fake_job_dict, fake_qobj


def _random_job(api):
    provider = QCticProvider(api=api)
    backend = provider.backends()[0]
    qobj = assemble(fake_circuit(), backend)
    job_id = str(uuid.uuid4())

    return QCticJob(backend, job_id, qobj)


def _build_api(httpserver, auth=True):
    api = QCticAPI(host=httpserver.url_for("/"))

    if auth:
        api.auth_token(str(uuid.uuid4()))

    return api


def test_error_no_auth(httpserver):
    job_dict = fake_job_dict()
    job_id = job_dict["job_id"]
    url = "/jobs/{}".format(job_id)
    httpserver.expect_request(url).respond_with_json(job_dict)
    api = _build_api(httpserver, auth=False)

    with pytest.raises(Exception):
        api.get_job_sync(job_id)

    api.auth_token(str(uuid.uuid4()))

    assert api.get_job_sync(job_id)


def test_get_job(httpserver):
    job_dict = fake_job_dict()
    job_id = job_dict["job_id"]
    url = "/jobs/{}".format(job_id)
    httpserver.expect_request(url).respond_with_json(job_dict)
    api = _build_api(httpserver)
    res = api.get_job_sync(job_id)

    assert res["job_id"] == job_id
    assert res["qobj"]


def test_get_jobs(httpserver):
    job_dicts = [fake_job_dict() for _ in range(5)]
    httpserver.expect_request("/jobs").respond_with_json(job_dicts)
    api = _build_api(httpserver)
    res = api.get_jobs_sync(limit=len(job_dicts), skip=0)

    assert len(res) == len(job_dicts)
    assert all(item.get("job_id", False) for item in res)


def test_get_jobs_arg_status(httpserver):
    job_dicts = [fake_job_dict() for _ in range(50)]

    def handler(req):
        return Response(json.dumps([
            item for item in job_dicts
            if item["status"] in req.args.getlist("status")
        ]))

    httpserver.expect_request("/jobs").respond_with_handler(handler)
    api = _build_api(httpserver)

    status_str = job_dicts[0]["status"]

    res = api.get_jobs_sync(
        limit=len(job_dicts),
        skip=0,
        status=status_str)

    assert all(item["status"] == status_str for item in res)

    status_all = list(set(item["status"] for item in job_dicts))
    limit_idx = len(status_all) - 1 if len(status_all) > 0 else 1
    status_list = status_all[:limit_idx]

    res = api.get_jobs_sync(
        limit=len(job_dicts),
        skip=0,
        status=status_list)

    assert all(item["status"] in status_list for item in res)


def test_get_backend_status(httpserver):
    httpserver.expect_request("/status").respond_with_json({
        "operational": True,
        "pending_jobs": 10
    })

    api = _build_api(httpserver)
    res = api.get_backend_status_sync()

    assert res.get("operational")
    assert res.get("pending_jobs")


def test_post_job(httpserver):
    api = _build_api(httpserver)
    job = _random_job(api)

    def handler(req):
        data = json.loads(req.data)
        assert data["job_id"]
        assert data["qobj"]
        return Response()

    httpserver.expect_request("/jobs").respond_with_handler(handler)
    api.post_job_sync(job)


def test_cancel_job(httpserver):
    api = _build_api(httpserver)
    job = _random_job(api)

    def handler(req):
        data = json.loads(req.data)
        assert data["status"] == JobStatus.CANCELLED.name
        return Response()

    url = "/jobs/{}".format(job.job_id())
    httpserver.expect_request(url).respond_with_handler(handler)
    api.cancel_job_sync(job.job_id())


def test_host_no_scheme():
    host = "192.168.0.1:9090"
    api = QCticAPI(host=host)
    assert re.match(r"^.+://.+$", api.host)

    host_scheme = "http://{}/".format(host)
    api_scheme = QCticAPI(host=host_scheme)
    assert api_scheme.host is host_scheme
