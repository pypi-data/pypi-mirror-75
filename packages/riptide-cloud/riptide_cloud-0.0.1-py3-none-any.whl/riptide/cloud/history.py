"""
Copyright (c) 2020 Riptide
"""
import json
from datetime import datetime
from typing import Any, List

from riptide.cloud.exception import RiptideClientException

_ROUTE = "api/history"

_MAX_IDENTIFIERS = 50
_MAX_TIME_DIFF = 31         # days


class RiptideHistoryApp:
    """
    Raw Historic Data - The value of a point as recorded at the site at
    various instances of time.

    Interpolated Historic Data - The value of a point as recorded at the
    site at various instances of time and also the estimated or interpolated
    values of the point for the missing periods by using re-sampling technique.

    Rolled-up Historic Data - The value of point condensed for a time period
    (e.g. 1 day, 10 days, 1 week and so on).

    Digested Historic Data - The value of a point summarized over a period of
    period of time (e.g. mean, sum, median and so on). This also allows user
    to apply a function on every value of a point like say add, subtract etc.
    """

    def __init__(self, client):
        self._client = client

    def get_history(self,
                    identifiers: List[str],
                    start: datetime,
                    end: datetime,

                    # Optional: Raw Historic Data.
                    reverse: bool = None,
                    limit: int = None,
                    output_tz: str = None,
                    response_format: str = None,
                    align_data: bool = None,

                    # Optional: Interpolated Historic Data.
                    interpolate: bool = None,
                    period: int = None,

                    # Optional: Rolled-up Historic Data.
                    rollup: bool = None,
                    freq: str = None,
                    how: str = None,

                    # Optional: Digested Historic Data.
                    func: Any = None) -> dict:
        """
        Retrieve history data.

        # Mandatory parameters
        :param identifiers: List of one-or-more entity property URIs.
        :param start: Datetime object.
        :param end: Datetime object.

        # Optional parameters: Raw Historic Data.
        :param limit: Maximum number of rows to return. Default is None in
        which case there is no upper limit.
        :param reverse: reverse=False will return the top `limit` number of
        rows. reverse=True will return the bottom `limit` number of rows.
        Defaults is False.
        :param output_tz: The timezone which the output data should be
        converted to. Default is None which means UTC.
        :param response_format: "default", "ordered_history",
        "compact_ordered_history", "ordered_list". Default is "default".
        :param align_data: Sort the underlying DataFrame based on its index.
        Default is False.

        # Optional parameters: Interpolated Historic Data.
        :param interpolate: A Boolean value indicating whether or not the
        data should be interpolated (re-sampled). If set to False, the raw
        history records are returned. Default is False.
        :param period: (used only when `interpolate` is True). The frequency
        at which to generate samples.

        # Optional parameters: Rolled-up Historic Data
        :param rollup: rollup=False will retrieve raw historic data.
        rollup=True will provide rolled-up historic data. Default is False.
        :param freq: (used only when `rollup` is True). The frequency
        at which to generate rollup records.
        Frequency Alias     Description
        B                   business day frequency
        D                   calendar day frequency
        W                   weekly frequency
        M                   month end frequency
        BM                  business month end frequency
        MS                  month start frequency
        BMS                 business month start frequency
        Q                   quarter end frequency
        BQ                  business quarter endfrequency
        QS                  quarter start frequency
        BQS                 business quarter start frequency
        A                   year end frequency
        BA                  business year end frequency
        AS                  year start frequency
        BAS                 business year start frequency
        H                   hourly frequency
        T                   minutely frequency
        S                   secondly frequency
        L                   milliseonds
        U                   microseconds
        :param how: (used only when `rollup` is True). Method for down- or
        re-sampling. Can be one of the following strings: "sum", "mean",
        "std", "max", "min", "median", "first", "last", "ohlc".

        # Optional parameters: Digested Historic Data.
        :param func: History digest function.

        :return: History data in JSON format.
        """

        if len(identifiers) > _MAX_IDENTIFIERS:
            raise RiptideClientException(
                "Length of identifiers must not exceed {}; "
                "Received {}".format(_MAX_IDENTIFIERS, len(identifiers))
            )

        if start > end:
            raise RiptideClientException(
                "start must not be greater than end; start={}, "
                "end={}".format(start, end)
            )

        if (end - start).days > _MAX_TIME_DIFF:
            raise RiptideClientException(
                "You cannot retrieve more than {} days of historical "
                "data.".format(_MAX_TIME_DIFF)
            )

        params = {
            "uris": json.dumps(identifiers),
            "start": start.replace(microsecond=0),
            "end": end.replace(microsecond=0)
        }
        if reverse is not None:
            params["reverse"] = reverse
        if limit is not None:
            params["limit"] = limit
        if output_tz is not None:
            params["output_tz"] = output_tz
        if response_format is not None:
            params["response_format"] = response_format
        if align_data is not None:
            params["align_data"] = align_data
        if interpolate is not None:
            params["interpolate"] = interpolate
        if period is not None:
            params["period"] = period
        if rollup is not None:
            params["rollup"] = rollup
        if freq is not None:
            params["freq"] = freq
        if how is not None:
            params["how"] = how
        if func is not None:
            params["func"] = func

        return self._client.rc_get(uri=_ROUTE, params=params)


# __END__
