"""
Copyright (c) 2020 Riptide
"""
from http.client import responses


class RiptideClientException(Exception):
    pass


class RiptideCloudException(Exception):

    def __init__(self, response):
        self._response = response
        super(RiptideCloudException, self).__init__(
            response.request.method, response.request.url,
            response.status_code, responses[response.status_code]
        )

    def _get_response_msg(self, response):
        return "{} {} -> {} ({})".format(
            response.request.method, response.request.url,
            response.status_code, responses[response.status_code]
        )

    def __repr__(self):
        return "<{} at {} {}>".format(
            self.__class__.__name__, hex(id(self)),
            self._get_response_msg(self._response)
        )

    def to_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "method": self._response.request.method,
            "url": self._response.request.url,
            "status_code": self._response.status_code,
            "status": responses[self._response.status_code],
            "text": self._response.text
        }


# __END__
