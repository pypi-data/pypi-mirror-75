import time
from typing import Optional, Dict, Any, Callable
import requests

from cryptocompsdk.config import MAX_LIMIT_PER_API_CALL
from cryptocompsdk.response import ResponseException, ResponseAPIBase


class Request:

    def __init__(self, url: str, payload: Optional[Dict[str, Any]], response: requests.Response):
        self.url = url
        self.payload = payload
        self.response = response

    @property
    def json(self) -> dict:
        return self.response.json()


class APIBase:
    _exception_class = ResponseException

    def __init__(self, api_key: str, throttle: Optional[float] = None):
        self.api_key = api_key
        self.throttle = throttle

    def request(self, url: str, payload: Optional[Dict[str, Any]] = None) -> Request:
        api_key_dict = {'api_key': self.api_key}
        payload = self.filter_payload(payload)
        if payload is not None:
            payload.update(api_key_dict)
        else:
            payload = api_key_dict

        result = requests.get(url, params=payload)
        print(result.request.url)
        return Request(url, payload, result)

    def filter_payload(self, payload: Optional[Dict[str, Any]]):
        if payload is None:
            return payload

        # Remove None values as they were just defaults
        without_none = {key: value for key, value in payload.items() if value is not None}

        # Convert booleans into boolean strings that API is expecting
        with_str_bools = {key: _bool_to_str_if_bool(value) for key, value in without_none.items()}

        return with_str_bools

    def _get_one_or_paginated(self, url: str, payload: Optional[Dict[str, Any]] = None,
                              max_api_calls: Optional[int] = None,
                              limit_in_payload: bool = True, date_name: str = 'toTs'):
        """
        This method should be called in the subclass .get method

        :param url: url to request
        :param payload: data to send with request
        :param max_api_calls: limit on number of API calls
        :param limit_in_payload: whether to include the limit parameter in request payload
        :param date_name: name of date in payload
        :return:
        """
        if payload is not None and payload.get('limit') == 0:
            return self._get_with_pagination(
                url,
                payload=payload,
                max_api_calls=max_api_calls,
                limit_in_payload=limit_in_payload,
                date_name=date_name,
            )
        return self._get(url, payload=payload)

    def _get(self, url: str, payload: Optional[Dict[str, Any]] = None):
        if self.throttle is not None:
            time.sleep(self.throttle)
        data = self.request(url, payload)
        obj = self._class_factory(data.json)
        # isinstance dict added for development of api where class has not been set yet
        if isinstance(obj, dict):
            return obj
        if obj.has_error:
            if payload is not None:
                payload_str = f'payload {payload}'
            else:
                payload_str = 'no payload'
            raise self._exception_class(f'Requested {url} with {payload_str}, '
                                            f'got {data.json} as response')
        obj._request = data
        return obj

    def _get_with_pagination(self, url: str, payload: Dict[str, Any],
                             max_api_calls: Optional[int] = None,
                             limit_in_payload: bool = True, date_name: str = 'toTs'):
        if max_api_calls is None:
            # TODO [#4]: less hackish
            max_api_calls = 10000000

        if limit_in_payload:
            payload['limit'] = MAX_LIMIT_PER_API_CALL

        end_time = payload[date_name]
        i = -1
        while i + 1 < max_api_calls:
            i += 1
            payload[date_name] = end_time
            try:
                data = self._get(url, payload)
            except self._exception_class as e:
                # In blockchain history API, upon going too far back, it sends this message back
                if 'does not have data available before requested timestamp' in str(e):
                    break
                else:
                    raise e
            if i == 0:
                all_data = data
            if data.is_empty:
                # In price history API, upon going too far back, it sends 0 for all data
                break
            if i != 0:
                # chop off matching record. The end_time observation will be included in both responses
                data.delete_record_matching_time(end_time)
                all_data = data + all_data
            end_time = data.time_from

        all_data.trim_empty_records_at_beginning()

        return all_data

    def _class_factory(self, data: dict):
        raise NotImplementedError('must implement in subclass')


def _bool_to_str(boolean: bool) -> str:
    if not isinstance(boolean, bool):
        raise ValueError(f'non-boolean {boolean} passed to _bool_to_str')

    if boolean:
        return 'true'

    return 'false'


def _bool_to_str_if_bool(obj: Any) -> Any:
    if not isinstance(obj, bool):
        return obj
    return _bool_to_str(obj)
