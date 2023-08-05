import logging
import os

from qiskit.providers import BaseProvider
from qiskit.providers.providerutils import filter_backends

from qctic.api import QCticAPI
from qctic.backend import (QCticQasmSimulator, QCticStatevectorSimulator,
                           QCticUnitarySimulator)

_logger = logging.getLogger(__name__)


class QCticProvider(BaseProvider):
    """Provider for CTIC Erwin backends."""

    ENV_HOST = "QCTIC_HOST"
    ENV_USERNAME = "QCTIC_USERNAME"
    ENV_PASSWORD = "QCTIC_PASSWORD"
    ENV_TOKEN = "JUPYTERHUB_API_TOKEN"

    def __init__(self, *args, **kwargs):
        self._api = kwargs.pop("api")

        if not self._api:
            raise Exception("Must set the api kwarg")

        super().__init__(args, kwargs)

        self._backends = [
            QCticQasmSimulator(provider=self),
            QCticStatevectorSimulator(provider=self),
            QCticUnitarySimulator(provider=self)
        ]

    @classmethod
    def from_env(cls, *args, **kwargs):
        host = os.getenv(cls.ENV_HOST, None)
        username = os.getenv(cls.ENV_USERNAME, None)
        password = os.getenv(cls.ENV_PASSWORD, None)
        token = os.getenv(cls.ENV_TOKEN, None)

        err_msg = "Missing Erwin environment variables: {}".format({
            cls.ENV_HOST: host,
            cls.ENV_USERNAME: username,
            cls.ENV_PASSWORD: password,
            cls.ENV_TOKEN: token
        })

        if not host:
            _logger.warning(err_msg)
            raise Exception(err_msg)

        api = QCticAPI(host=host)

        if username and password:
            api.auth_basic(username, password)
        elif token:
            api.auth_token(token)
        else:
            _logger.warning(err_msg)
            raise Exception(err_msg)

        return cls(api=api, *args, **kwargs)

    @property
    def api(self):
        return self._api

    def get_backend(self, name=None, **kwargs):
        return super().get_backend(name=name, **kwargs)

    def backends(self, name=None, filters=None, **kwargs):
        backends = self._backends

        if name:
            backends = [
                backend for backend in backends
                if backend.name() == name
            ]

        return filter_backends(backends, filters=filters, **kwargs)

    def __str__(self):
        return self.__class__.__name__
