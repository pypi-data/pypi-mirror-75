"""
Copyright (c) 2020 Riptide
"""
from datetime import datetime
from typing import List

from riptide.cloud.exception import RiptideClientException

_ROUTE = "api/alarms"


class RiptideAlarmApp:

    def __init__(self, client):
        self._client = client

        # TODO: this should be typing.Literal
        self._context = ["site_uuids", "entity_uuids", "point_uuids", "uuids"]

    def get_alarm(self, alarm_uuid: str) -> dict:
        """
        Get alarm information.

        :param alarm_uuid: alarm UUID.
        :return: JSON response.
        """
        return self._client.rc_get(uri="{}/{}".format(_ROUTE, alarm_uuid))

    def get_alarm_history(self,
                          uuids: List[str],
                          context: str,
                          start: datetime = None,
                          end: datetime = None) -> List[dict]:
        """
        Retrieve alarms historical data.

        :param uuids: list of uuids.
        :param context: valid values are "site_uuids", "entity_uuids",
        "point_uuids", "uuids" (alarm uuids).
        :param start: datetime object.
        :param end: datetime object.
        :return: JSON response.
        """
        uri = "{}/history?{}={}".format(_ROUTE, context, ",".join(uuids))
        if context not in self._context:
            raise RiptideClientException(
                "context must be one of the following - "
                "{}".format(self._context)
            )
        if start:
            uri = "{}&start={}".format(uri, start)
        if end:
            uri = "{}&end={}".format(uri, end)
        return self._client.rc_get(uri=uri)


# __END__
