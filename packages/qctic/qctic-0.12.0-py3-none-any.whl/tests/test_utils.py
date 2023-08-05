import json
import time
from datetime import datetime, timedelta, timezone

import pytest
from qiskit import Aer, execute
from qiskit.assembler import disassemble
from qiskit.providers import JobStatus
from werkzeug.wrappers import Response

from qctic.utils import QcticResultTimeoutError, wait_result, wait_result_async

_RESULT_SLEEP = 0.25


def _mock_simulator_result(job, httpserver, latency=_RESULT_SLEEP):
    circuits, _run_config, _user_qobj_header = disassemble(job.qobj())
    simulator = Aer.get_backend("qasm_simulator")
    simulator_job = execute(circuits, simulator)
    simulator_result = simulator_job.result()
    url = "/jobs/{}".format(job.job_id())
    dtime_now = datetime.now(timezone.utc)
    dtime_end = dtime_now + timedelta(seconds=latency)
    tstamp_end = dtime_now.timestamp() + latency

    job_dict = {
        "job_id": job.job_id(),
        "qobj": job.qobj().to_dict(),
        "date_submit": dtime_now.isoformat(),
        "date_start": dtime_now.isoformat(),
        "status": JobStatus.RUNNING.name
    }

    def handler(req):
        job_res = {**job_dict}

        if time.time() >= tstamp_end:
            job_res.update({
                "date_end": dtime_end.isoformat(),
                "status": JobStatus.DONE.name,
                "result": simulator_result.to_dict()
            })

        return Response(json.dumps(job_res))

    httpserver.expect_request(url).respond_with_handler(handler)

    return simulator_result


def test_wait_result(job, httpserver):
    simulator_result = _mock_simulator_result(job, httpserver)
    result = wait_result(job, base_sleep=_RESULT_SLEEP)
    assert result.to_dict() == simulator_result.to_dict()


@pytest.mark.asyncio
async def test_wait_result_async(job, httpserver):
    simulator_result = _mock_simulator_result(job, httpserver)
    result = await wait_result_async(job, base_sleep=_RESULT_SLEEP)
    assert result.to_dict() == simulator_result.to_dict()


@pytest.mark.asyncio
async def test_wait_timeout(job, httpserver):
    base_sleep = 0.1
    sleep_growth = 1.0
    timeout = base_sleep
    latency = base_sleep * 20.0

    _mock_simulator_result(job, httpserver, latency=latency)

    with pytest.raises(QcticResultTimeoutError):
        await wait_result_async(
            job,
            base_sleep=base_sleep,
            timeout=timeout,
            sleep_growth=sleep_growth)
