from qiskit.providers import JobStatus

from qctic.schemas import GetJobsQuerySchema


def test_get_jobs_query():
    limit = 15

    jobs_query = GetJobsQuerySchema().dump({
        "limit": limit
    })

    assert jobs_query["limit"] is limit
    assert jobs_query.get("status", None) is None

    status_str = JobStatus.RUNNING.name

    jobs_query = GetJobsQuerySchema().dump({
        "limit": limit,
        "status": status_str
    })

    assert jobs_query["limit"] is limit
    assert jobs_query["status"] == [status_str]

    status_list = [
        JobStatus.RUNNING.name,
        JobStatus.DONE.name
    ]

    jobs_query = GetJobsQuerySchema().dump({
        "limit": limit,
        "status": status_list
    })

    assert jobs_query["limit"] is limit
    assert jobs_query["status"] == status_list
