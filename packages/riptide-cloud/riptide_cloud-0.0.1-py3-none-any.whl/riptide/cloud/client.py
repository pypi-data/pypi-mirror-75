"""
Copyright (c) 2020 Riptide
"""
import json
import logging
from http import HTTPStatus
from http.client import responses

import requests
from requests.auth import HTTPBasicAuth

from riptide.cloud.exception import RiptideCloudException

_LOGGER = logging.getLogger(__name__)


__all__ = ["RiptideCloudClient"]


class RiptideCloudClient:

    def __init__(self, config=None, config_file=None):
        self._config = config or {}
        self._config_file = config_file

        self._scheme = None
        self._hostname = None
        self._port = None
        self._timeout = None
        self._auth = None
        self._url = None

        if config_file:
            self._read_config_file()
        self._initialize(config=self._config)

    def __repr__(self):
        return "<{} at {} url={}>".format(
            self.__class__.__name__, hex(id(self)), self._url
        )

    def _read_config_file(self):
        with open(self._config_file) as fp:
            self._config = json.load(fp)

    def _initialize(self, config):

        if not config:
            return

        self._scheme = config.get("scheme", "https")
        self._hostname = config.get("hostname", "app.riptideio.com")
        self._port = config.get("port", 443)

        self._timeout = int(config.get("timeout", 60))

        _username = config.get("username")
        _password = config.get("password")
        _auth = config.get("auth")

        if not _auth:
            raise Exception("Unknown auth type")

        if _auth and _auth.lower() == "basic":
            if not _username:
                raise Exception("username required")
            if not _password:
                raise Exception("password required")
            # TODO: Add test for username ends with riptideio.com, etc.
            self._auth = HTTPBasicAuth(_username, _password)

        self._url = "{}://{}:{}/".format(
            self._scheme, self._hostname, self._port
        )

    def _get_response_msg(self, response):
        return "{} {} -> {} ({})".format(
            response.request.method, response.request.url,
            response.status_code, responses[response.status_code]
        )

    def _parse_response(self, response):

        _LOGGER.debug(self._get_response_msg(response=response))

        if response.status_code == HTTPStatus.OK.value:
            try:
                data = response.json()
                if "result" in data:
                    data = data["result"]
                return data
            except Exception:
                _LOGGER.error(
                    "Unable to decode response text: {}".format(response.text)
                )
                raise

        if response.status_code == HTTPStatus.NO_CONTENT.value:
            return

        raise RiptideCloudException(response=response)

    def rc_get(self, uri, headers=None, params=None, timeout=None):
        _LOGGER.debug("uri={}, headers={}, params={}, timeout={}".format(
            uri, headers, params, timeout
        ))
        return self._parse_response(
            requests.get(
                self._url + uri,
                headers=headers,
                params=params,
                timeout=timeout or self._timeout,
                auth=self._auth
            )
        )

    def rc_put(self, uri, data, headers=None, timeout=None):
        return self._parse_response(
            requests.put(
                self._url + uri,
                data=data,
                headers=headers,
                timeout=timeout or self._timeout,
                auth=self._auth
            )
        )

    def rc_post(self, uri, data, headers=None, timeout=None):
        return self._parse_response(
            requests.post(
                self._url + uri,
                data=data,
                headers=headers,
                timeout=timeout or self._timeout,
                auth=self._auth
            )
        )

    def rc_delete(self, uri, headers=None, timeout=None):
        return self._parse_response(
            requests.delete(
                self._url + uri,
                headers=headers,
                timeout=timeout or self._timeout,
                auth=self._auth
            )
        )


# __END__
