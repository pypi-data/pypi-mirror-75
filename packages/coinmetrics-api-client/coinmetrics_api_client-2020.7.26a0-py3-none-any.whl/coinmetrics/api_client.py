import socket
from datetime import datetime, date
from logging import getLogger
from typing import Dict, Union, List, Any, Optional, cast
from urllib.parse import urlencode

import requests
from requests import HTTPError

from coinmetrics._utils import transform_url_params_values_to_str, retry

try:
    import ujson as json
except ImportError:
    # fall back to std json package
    import json  # type: ignore

from coinmetrics._typing import DATA_RETURN_TYPE
from coinmetrics.constants import (
    ApiBranch,
    PagingFrom,
    API_BASE,
    COMMUNITY_API_BRANCHES,
)
from coinmetrics._data_collection import DataCollection

logger = getLogger("cm_client")


class CoinMetricsClient:
    def __init__(
        self,
        api_key: str = "",
        api_branch: ApiBranch = ApiBranch.PRODUCTION,
        page_size: int = 1000,
    ):
        if not api_key or not isinstance(api_key, (str, bytes)):
            if api_branch not in COMMUNITY_API_BRANCHES:
                raise ValueError("API key must be a non empty string")
        self._page_size = page_size
        self._api_key_url_str = (
            "api_key={}".format(api_key)
            if api_branch not in COMMUNITY_API_BRANCHES
            else ""
        )
        self._api_base_url = "{}/v4".format(API_BASE[api_branch])

    def catalog_assets(
        self, assets: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about assets.

        :param assets: A single asset or a list of assets to return info for.
        If no assets provided, all available assets are returned.
        :return: Information that is available for requested assets, like: Full name, metrics and available frequencies,
        markets, exchanges, etc.
        """

        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/assets", {"assets": assets})["data"],
        )

    def catalog_exchanges(
        self, exchanges: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about exchanges.

        :param exchanges: A single exchange name or a list of exchanges to return info for.
        If no exchanges provided, all available exchanges are returned.
        :return: Information that is available for requested exchanges, like: markets, min and max time available.
        """
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/exchanges", {"exchanges": exchanges})["data"],
        )

    def catalog_indexes(
        self, indexes: Optional[Union[List[str], str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Returns meta information about indexes.

        :param indexes: A single index name or a list of indexes to return info for.
        If no indexes provided, all available indexes are returned.
        :return: Information that is available for requested indexes, like: Full name, and available frequencies.
        """
        return cast(
            List[Dict[str, Any]],
            self._get_data("catalog/indexes", {"indexes": indexes})["data"],
        )

    def catalog_markets(
        self,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        quote: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns list of markets that correspond to a filter, if no filter is set, returns all available asset.

        :param exchange: name of the exchange
        :param base: name of base asset
        :param quote: name of quote asset
        :param asset: name of either base or quote asset
        :param symbol: name of a symbol. Usually used for futures contracts.
        :return: Information about markets that correspond to a filter along with meta information like:
        type of market and min and max available time frames.
        """
        params: Dict[str, Any] = {
            "exchange": exchange,
            "base": base,
            "quote": quote,
            "asset": asset,
            "symbol": symbol,
        }
        return cast(
            List[Dict[str, Any]], self._get_data("catalog/markets", params)["data"]
        )

    def catalog_metrics(
        self,
        metrics: Optional[Union[List[str], str]] = None,
        reviewable: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns list of available metrics along with information for them like
        description, category, precision and assets for which a metric is available.

        :param metrics: A single metric name or a list of metrics to return info for.
        If no metrics provided, all available metrics are returned.
        :param reviewable: Show only reviewable or non-reviewable by human metrics. By default all metrics are shown.
        :return: Information about metrics that correspond to a filter along with meta information like:
        description, category, precision and assets for which a metric is available.
        """
        params: Dict[str, Any] = {"metrics": metrics, "reviewable": reviewable}
        return cast(
            List[Dict[str, Any]], self._get_data("catalog/metrics", params)["data"]
        )

    def get_index_levels(
        self,
        indexes: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        """
        Returns index levels for a specified indexes and date range.

        :param indexes: list of index names
        :param frequency: frequency of the returned timeseries, for e.g 15s, 1d, etc.
        :param page_size: number of items returned per page,
        typically you don't want to change this parameter unless you are interested in a first retuned item only.
        :param paging_from: Defines where you want to start receiving items from, 'start' or 'end' of the timeseries.
        :param start_time: Start time of the timeseries.
        :param end_time: End time of the timeseries.
        :param start_inclusive: Flag to define if start timestamp must be included in the timeseries if present.
        :param end_inclusive: Flag to define if end timestamp must be included in the timeseries if present.
        :param timezone: timezone of the start/end times in db format for example: "America/Chicago".
        Default value is "UTC". For more details check out API documentation page.
        :return: Index Levels timeseries.
        """

        params: Dict[str, Any] = {
            "indexes": indexes,
            "frequency": frequency,
            "page_size": page_size or self._page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/index-levels", params)

    def get_market_candles(
        self,
        markets: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        params: Dict[str, Any] = {
            "markets": markets,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/market-candles", params)

    def get_market_trades(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/market-trades", params)

    def get_market_quotes(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/market-quotes", params)

    def get_market_orderbooks(
        self,
        markets: Union[List[str], str],
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        params: Dict[str, Any] = {
            "markets": markets,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/market-orderbooks", params)

    def get_asset_metrics(
        self,
        assets: Union[List[str], str],
        metrics: Union[List[str], str],
        frequency: Optional[str] = None,
        page_size: Optional[int] = None,
        paging_from: Optional[Union[PagingFrom, str]] = None,
        start_time: Optional[Union[datetime, date, str]] = None,
        end_time: Optional[Union[datetime, date, str]] = None,
        start_inclusive: Optional[bool] = None,
        end_inclusive: Optional[bool] = None,
        timezone: Optional[str] = None,
    ) -> DataCollection:
        params: Dict[str, Any] = {
            "assets": assets,
            "metrics": metrics,
            "frequency": frequency,
            "page_size": page_size,
            "paging_from": paging_from,
            "start_time": start_time,
            "end_time": end_time,
            "start_inclusive": start_inclusive,
            "end_inclusive": end_inclusive,
            "timezone": timezone,
        }
        return DataCollection(self._get_data, "timeseries/asset-metrics", params)

    def _get_data(self, url: str, params: Dict[str, Any]) -> DATA_RETURN_TYPE:
        if params:
            params_str = "&{}".format(
                urlencode(transform_url_params_values_to_str(params))
            )
        else:
            params_str = ""

        actual_url = "{}/{}?{}{}".format(
            self._api_base_url, url, self._api_key_url_str, params_str
        )
        resp = self._send_request(actual_url)
        try:
            data = json.loads(resp.content)
        except ValueError:
            resp.raise_for_status()
            raise
        else:
            if "error" in data:
                logger.error(
                    "error found for the query: %s, error content: %s", actual_url, data
                )
                resp.raise_for_status()
            return cast(DATA_RETURN_TYPE, data)

    @retry((socket.gaierror, HTTPError), retries=5, wait_time_between_retries=5)
    def _send_request(self, actual_url):
        return requests.get(actual_url)
