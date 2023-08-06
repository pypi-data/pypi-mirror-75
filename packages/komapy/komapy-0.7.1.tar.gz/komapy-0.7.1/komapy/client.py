"""
KomaPy data fetcher and reader.
"""

import json
import bmaclient

from uuid import uuid4
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen

from . import exceptions, processing
from .settings import app_settings


def set_api_protocol(protocol):
    """
    Set BMA API protocol, either http or https.

    :param protocol: BMA API protocol
    :type protocol: str
    """
    if not protocol:
        raise ValueError('Protocol name cannot be None or empty')

    app_settings.BMA_API_PROTOCOL = protocol.lower()


def set_api_key(key):
    """
    Set BMA API key to enable accessing the API.

    :param key: BMA API key.
    :type key: str
    """
    if not key:
        raise ValueError('API key cannot be None or empty')

    app_settings.BMA_API_KEY = key


def set_access_token(token):
    """
    Set BMA access token to enable accessing the API.

    :param token: BMA API access token.
    :type token: str
    """
    if not token:
        raise ValueError('Access token cannot be None or empty')

    app_settings.BMA_ACCESS_TOKEN = token


def set_timezone(name):
    """
    Set app timezone setting.

    :param name: Time zone name, e.g. Asia/Jakarta.
    :type name: str
    """
    if not name:
        raise ValueError('Timezone name cannot be None or empty')

    app_settings.TIME_ZONE = name


def set_api_host(name):
    """
    Override BMA API default host.

    :param name: Host name or IP address.
    :type name: str
    """
    if not name:
        raise ValueError('API host cannot be None or empty')

    app_settings.BMA_API_HOST = name


def fetch_bma_as_dictionary(name, **params):
    """
    Make a request to the BMA API and return data as Python dictionary.

    :param name: BMA API name, e.g. doas, edm, tiltmeter, etc.
    :type name: str
    :param params: BMA field query filtering parameters.
    :type params: dict
    :return: Dictionary of resolved BMA API data.
    :rtype: dict
    """
    if app_settings.BMA_API_CLASS is not None:
        api = app_settings.BMA_API_CLASS(
            api_key=app_settings.BMA_API_KEY,
            access_token=app_settings.BMA_ACCESS_TOKEN)
    else:
        api = bmaclient.MonitoringAPI(
            api_key=app_settings.BMA_API_KEY,
            access_token=app_settings.BMA_ACCESS_TOKEN)

    if app_settings.BMA_API_PROTOCOL:
        api.protocol = app_settings.BMA_API_PROTOCOL

    if app_settings.BMA_API_HOST:
        api.host = app_settings.BMA_API_HOST

    if app_settings.IGNORE_BMA_REQUEST_CACHE:
        params.update(rv=uuid4().hex)

    method = api.get_fetch_method(name)
    if not method:
        raise exceptions.ChartError('Unknown parameter name {}'.format(name))
    return method(**params)


def fetch_bma_as_dataframe(name, **params):
    """
    Make a request to the BMA API and return data as Pandas DataFrame.

    :param name: BMA API name, e.g. doas, edm, tiltmeter, etc.
    :type name: str
    :param params: BMA field query filtering parameters.
    :type params: dict
    :return: :class:`pandas.DataFrame` of resolved BMA API data.
    :rtype: :class:`pandas.DataFrame`
    """
    response = fetch_bma_as_dictionary(name, **params)
    return processing.dataframe_from_dictionary(response)


def fetch_url_as_dictionary(url, **params):
    """
    Make a request to the URL and return data as Python dictionary.

    :param url: URL that returns JSON data.
    :type url: str
    :param params: URL query filtering parameters.
    :type params: dict
    :return: Dictionary of resolved URL content.
    :rtype: dict
    """
    full_query_params = '?{}'.format(urlencode(params)) if params else ''
    full_url_with_params = '{url}{query_params}'.format(
        url=url,
        query_params=full_query_params
    )

    with urlopen(full_url_with_params) as content:
        data = json.loads(content.read().decode('utf-8'))

    return data


def fetch_url_as_dataframe(url, **params):
    """
    Make a request to the URL and return data as Pandas DataFrame.

    :param url: URL that returns JSON data.
    :type url: str
    :param params: URL query filtering parameters.
    :type params: dict
    :return: :class:`pandas.DataFrame` of resolved URL content.
    :rtype: :class:`pandas.DataFrame`
    """
    response = fetch_url_as_dictionary(url, **params)
    return processing.dataframe_from_dictionary(response)
