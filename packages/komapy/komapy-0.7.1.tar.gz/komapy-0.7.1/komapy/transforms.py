"""
KomaPy data transforms module.
"""

from collections import Callable

import pandas as pd

from .client import fetch_bma_as_dataframe
from .decorators import register_as_decorator
from .exceptions import ChartError

transform_registers = {
    # Legacy names.
    'slope_correction': 'slope_correction',

    # Register all functions with namespace prefix.
    'komapy.transforms.slope_correction': 'slope_correction',
}


@register_as_decorator
def register_transform(name, resolver, **kwargs):
    """
    Register data transform function.

    :param name: Name of transform register.
    :type name: str
    :param resolver: Transform callable resolver function.
    :type resolver: :class:`collections.Callable`
    """
    if not isinstance(resolver, Callable):
        raise ChartError('Data transform resolver must be callable')

    if name in transform_registers:
        raise ChartError(
            'Data transform {} already exists in the global register names. '
            'Use different name or use namespace prefix.'.format(name))

    transform_registers[name] = resolver


def unregister_transform(name):
    return transform_registers.pop(name, None)


def slope_correction(data, config):
    """
    Apply EDM slope distance correction.
    """
    if config.name != 'edm':
        return data

    timestamp__gte = config.query_params.get(
        'timestamp__gte') or config.query_params.get('start_at')
    timestamp__lt = config.query_params.get(
        'timestamp__lt') or config.query_params.get('end_at')

    err_data = fetch_bma_as_dataframe('slope', **{
        'timestamp__gte': timestamp__gte,
        'timestamp__lt': timestamp__lt,
        'benchmark': config.query_params['benchmark'],
        'reflector': config.query_params['reflector'],
    })
    if err_data.empty:
        return data

    slope_data = pd.DataFrame()
    slope_data['timestamp'] = data[0]
    slope_data['slope_distance'] = data[1]

    corrected_data = slope_data.apply(
        lambda item: item.slope_distance + err_data.where(
            err_data.timestamp > item.timestamp).deviation.sum(), axis=1)
    return [data[0], corrected_data]
