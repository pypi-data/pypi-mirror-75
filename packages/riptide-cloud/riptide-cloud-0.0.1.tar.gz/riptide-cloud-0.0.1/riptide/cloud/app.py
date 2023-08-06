"""
Copyright (c) 2020 Riptide
"""
import logging

from riptide.cloud.alarms import RiptideAlarmApp
from riptide.cloud.client import RiptideCloudClient
from riptide.cloud.entity import RiptideEntityApp
from riptide.cloud.history import RiptideHistoryApp
from riptide.cloud.watch import RiptideWatchApp

_LOGGER = logging.getLogger(__name__)


__all__ = ["RiptideCloudApp"]


class RiptideCloudApp:

    def __init__(self, config=None, config_file=None, **kwargs):

        self._client = RiptideCloudClient(
            config=config, config_file=config_file
        )

        self._alarms = RiptideAlarmApp(client=self._client)
        self._entity = RiptideEntityApp(client=self._client)
        self._history = RiptideHistoryApp(client=self._client)
        self._watch = RiptideWatchApp(client=self._client)

    @property
    def alarms(self):
        return self._alarms

    @property
    def entity(self):
        return self._entity

    @property
    def history(self):
        return self._history

    @property
    def watch(self):
        return self._watch


# __END__
