import asyncio
import datetime
import logging
import re
from functools import wraps
from textwrap import shorten
from urllib.parse import urljoin

from qiskit.providers import JobStatus
from tornado.escape import json_decode, json_encode
from tornado.httpclient import (AsyncHTTPClient, HTTPClient, HTTPError,
                                HTTPRequest)
from tornado.httputil import url_concat

from qctic.schemas import BackendStatusSchema, GetJobsQuerySchema, JobSchema

_SCHEME_REGEX = r"^.+://.*"
_SCHEME_DEFAULT = "http"
_BODY_WIDTH = 1024

_logger = logging.getLogger(__name__)


def _format_req(req):
    base = "{} {}".format(req.method, req.url)
    body = shorten(req.body.decode(), width=_BODY_WIDTH) if req.body else None
    return "{}\n{}".format(base, body) if body else base


class QCticAPIError(Exception):
    pass


class QCticAPI:
    """Class that represents the Erwin simulation API interface."""

    DEFAULT_HOST = "http://localhost"

    def __init__(self, host=DEFAULT_HOST):
        """Constructor.

        Args:
            host (str): (Optional) URL of the API server (``http://localhost`` by default).
        """

        if not re.match(_SCHEME_REGEX, host):
            _logger.debug(
                "Host '%s' has no scheme: Using '%s' by default",
                host, _SCHEME_DEFAULT)

            host = "{}://{}".format(_SCHEME_DEFAULT, host)

        self._req_defaults = {"headers": {"Content-Type": "application/json"}}
        self._client = None
        self._host = host
        self._loop = None

        if not self._host.endswith("/"):
            self._host = f"{self._host}/"

    @property
    def loop(self):
        """asyncio.AbstractEventLoop: The event loop used by the sync methods of this class."""

        if self._loop:
            return self._loop

        try:
            return asyncio.get_running_loop()
        except (RuntimeError, AttributeError):
            pass

        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            # It seems we are not in the main thread,
            # thus the loop was not created implicitly.
            asyncio.set_event_loop(asyncio.new_event_loop())

        return asyncio.get_event_loop()

    @loop.setter
    def loop(self, val):
        self._loop = val

    @property
    def host(self):
        return self._host

    @property
    def client(self):
        """tornado.httpclient.AsyncHTTPClient: HTTP client."""

        if not self._client:
            self._client = AsyncHTTPClient()

        if not self.has_auth:
            raise Exception("Must authenticate first")

        return self._client

    @property
    def has_auth(self):
        """bool: True if the authentication arguments are defined."""

        token = self._req_defaults.get("headers", {}).get("Authorization")
        user = self._req_defaults.get("auth_username")
        passwd = self._req_defaults.get("auth_password")

        return token or (user and passwd)

    def _build_url(self, part):
        part = part if not part.startswith("/") else part[1:]
        return urljoin(self.host, part)

    def _clean_auth(self):
        self._req_defaults.pop("auth_username", None)
        self._req_defaults.pop("auth_password", None)
        self._req_defaults.get("headers", {}).pop("Authorization", None)

    def auth_token(self, token):
        """Update the HTTP client configuration to use *Bearer* authorization.

        Clears any authorization data that was previously defined.

        Args:
            token (str): API token.
        """

        self._clean_auth()

        self._req_defaults["headers"] = self._req_defaults.get("headers", {})

        self._req_defaults["headers"].update({
            "Authorization": "Bearer {}".format(token)
        })

    def auth_basic(self, user, passwd):
        """Update the HTTP client configuration to use *Basic* authorization.

        Clears any authorization data that was previously defined.

        Args:
            user (str): Username.
            passwd (str): Password.
        """

        self._clean_auth()

        self._req_defaults.update({
            "auth_username": user,
            "auth_password": passwd
        })

    def _request(self, **kwargs):
        request_params = {**self._req_defaults}
        request_params.update(kwargs)
        return HTTPRequest(**request_params)

    async def _fetch(self, *args, **kwargs):
        try:
            return await self.client.fetch(*args, **kwargs)
        except HTTPError as ex:
            err = json_decode(ex.response.body)
            _logger.warning("Error on API request: %s", err)
            err_msg = "[{}] {}".format(err.get("name"), err.get("description"))
            raise QCticAPIError(err_msg)

    async def get_job(self, job_id):
        """Retrieves a single Job from the API.

        Args:
            job_id (str): Job ID.

        Returns:
            dict: Dict that conforms to the ``JobSchema`` schema.
        """

        req = self._request(
            url=self._build_url("/jobs/{}".format(job_id)),
            method="GET")

        _logger.debug(_format_req(req))
        res = await self._fetch(req)
        job_dict = json_decode(res.body)

        if not job_dict:
            raise QCticAPIError("Job not found: {}".format(job_id))

        return JobSchema().load(job_dict)

    async def get_jobs(self, **kwargs):
        """Retrieves a set of Jobs from the API.

        Args:
            limit (int): (Optional) Maximum number of Jobs that should be returned.
            skip (int): (Optional) Skip this number of Jobs before adding them to the result set 
                (useful for pagination). Jobs are sorted by date_submit DESC by default.
            status (list(str)): (Optional) Set of status used as job filter.
            date_start (datetime): (Optional) Lower threshold for ``date_submit``.
            date_end (datetime): (Optional) Upper threshold for ``date_submit``.

        Returns:
            list(dict): List of dicts that conform to the ``JobSchema`` schema.
        """

        params = GetJobsQuerySchema().dump(kwargs)
        status = params.pop("status", [])
        url = url_concat(self._build_url("/jobs"), params)

        for item in status:
            url = url_concat(url, {"status": item})

        req = self._request(url=url, method="GET")

        _logger.debug(_format_req(req))
        res = await self._fetch(req)

        return [JobSchema().load(item) for item in json_decode(res.body)]

    async def get_backend_status(self):
        """Retrieves the current status of the simulation platform.

        Returns:
            dict: Dict that conforms to the ``BackendStatusSchema`` schema.
        """

        req = self._request(
            url=self._build_url("/status"),
            method="GET")

        _logger.debug(_format_req(req))
        res = await self._fetch(req)

        return BackendStatusSchema().load(json_decode(res.body))

    async def post_job(self, job):
        """Creates a new job in the simulation platform.

        Args:
            job (QCticJob): The job to be created.
        """

        job_init = {
            "qobj": job.qobj().to_dict(),
            "job_id": job.job_id(),
            "status": JobStatus.INITIALIZING.name,
            "date_submit": datetime.datetime.now(datetime.timezone.utc)
        }

        if job.run_params and len(job.run_params) > 0:
            job_init.update({"run_params": job.run_params})

        body = json_encode(JobSchema().dump(job_init))

        req = self._request(
            url=self._build_url("/jobs"),
            method="POST",
            body=body)

        _logger.debug(_format_req(req))
        await self._fetch(req)

    async def cancel_job(self, job_id):
        """Attempts to cancel a job that is currently active.

        Args:
            job_id (str): Job ID.
        """

        body = json_encode({"status": JobStatus.CANCELLED.name})

        req = self._request(
            url=self._build_url("/jobs/{}".format(job_id)),
            method="PUT",
            body=body)

        _logger.debug(_format_req(req))
        await self._fetch(req)

    def get_job_sync(self, job_id):
        """Synchronous version of the ``get_job`` method."""

        return self.loop.run_until_complete(self.get_job(job_id))

    def get_jobs_sync(self, **kwargs):
        """Synchronous version of the ``get_jobs`` method."""

        return self.loop.run_until_complete(self.get_jobs(**kwargs))

    def get_backend_status_sync(self):
        """Synchronous version of the ``get_backend_status`` method."""

        return self.loop.run_until_complete(self.get_backend_status())

    def post_job_sync(self, job):
        """Synchronous version of the ``post_job`` method."""

        return self.loop.run_until_complete(self.post_job(job))

    def cancel_job_sync(self, job_id):
        """Synchronous version of the ``cancel_job`` method."""

        return self.loop.run_until_complete(self.cancel_job(job_id))
