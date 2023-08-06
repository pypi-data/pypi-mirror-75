"""
Copyright (c) 2020 Riptide
"""
import json
from typing import List

_ROUTE = "api/watch"


class RiptideWatchApp:

    def __init__(self, client):
        self._client = client

    def create_watch(self, identifiers: List[str]) -> str:
        """
        Create a watch for the list of interested points.

        :param identifiers: list of entity property uri's.
        :return: watch id
        """
        return self._client.rc_put(uri=_ROUTE, data=json.dumps(identifiers))

    def get_watches(self) -> List[str]:
        """
        Get id's of all active watches.

        :return: list of one-or-more watch id's.
        """
        return self._client.rc_get(uri=_ROUTE)

    def poll_watch(self, watch_id: str) -> List[dict]:
        """
        Retrieve info for the given Watch.

        :param watch_id: watch id.
        :return: watch info.
        """
        return self._client.rc_get(uri="{}/{}".format(_ROUTE, watch_id))

    # TODO: testing (Not working - 500)
    def poll_watch_changed(self, watch_id: str) -> List[dict]:
        """
        Retrieve the most recently changed current values of the Entity
        properties associated with a particular Watch. Only the values that
        have changed since the last time the Watch was polled are returned.

        :param watch_id: watch id.
        :return: watch record for the changed points.
        """
        return self._client.rc_get(
            uri="{}/{}?cov=true".format(_ROUTE, watch_id)
        )

    def delete_watch(self, watch_id: str) -> dict:
        """
        Delete watch.

        :param watch_id: watch id to delete
        :return: nothing.
        """
        return self._client.rc_delete(uri="{}/{}".format(_ROUTE, watch_id))

    def read_present_value(self, identifier: str) -> dict:
        """
        Get present value of an entity property.

        :param identifier: entity property uri.
        :return: Current watch record for the given entity property
        """
        return self._client.rc_get(
            uri="{}/presentValue/{}".format(_ROUTE, identifier)
        )


# __END__
