"""
KomaPy processing engine.
"""

from collections import Callable

import numpy as np
import pandas as pd
from matplotlib import cm

from .decorators import register_as_decorator
from .exceptions import ChartError

supported_aggregations = {
    'cumsum': 'cumsum',
    'add': 'add',
    'subtract': 'subtract',
    'multiply': 'multiply',
    'divide': 'divide',
    'power': 'power',

    'sub': 'subtract',
    'mul': 'multiply',
    'div': 'divide',
    'pow': 'power'
}


@register_as_decorator
def register_aggregation(name, resolver, **kwargs):
    """
    Register data aggregation function.

    :param name: Name of aggregation register.
    :type name: str
    :param resolver: Aggregation callable resolver function.
    :type resolver: :class:`collections.Callable`
    """
    if not isinstance(resolver, Callable):
        raise ChartError('Data aggregation resolver must be callable')

    if name in supported_aggregations:
        raise ChartError(
            'Data aggregation {} already exists in the global register names. '
            'Use different name or use namespace prefix.'.format(name))

    supported_aggregations[name] = resolver


def unregister_aggregation(name):
    return supported_aggregations.pop(name, None)


def dataframe_from_dictionary(entry):
    """Create Pandas DataFrame from list of dictionary."""
    return pd.DataFrame(entry)


def empty_dataframe():
    """Create empty Pandas DataFrame."""
    return pd.DataFrame()


def dataframe_or_empty(data, name):
    """Get DataFrame column name or return empty DataFrame."""
    return data.get(name, empty_dataframe())


def read_csv(*args, **kwargs):
    """Read CSV file."""
    return pd.read_csv(*args, **kwargs)


def read_excel(*args, **kwargs):
    """Read Excel file."""
    return pd.read_excel(*args, **kwargs)


def read_json(*args, **kwargs):
    """Read JSON file."""
    return pd.read_json(*args, **kwargs)


def read_hdf(*args, **kwargs):
    """Read HDF file."""
    return pd.read_hdf(*args, **kwargs)


def read_sql(*args, **kwargs):
    """Read SQL query or database table."""
    return pd.read_sql(*args, **kwargs)


def get_rgb_color(num_sample, index, colormap='tab10'):
    """
    Get RGB color at current index for number of sample from matplotlib
    color map.
    """
    space = np.linspace(0, 1, num_sample)
    cmap = cm.get_cmap(colormap)
    return cmap(space[index])


def cumsum(data, params=None):
    """
    Cumulative sum function aggregation.

    Example config:

    .. code-block:: python

        config = {
            ...
            'fields': ['timestamp', 'energy'],
            'aggregations': [
                {
                    'func': 'cumsum',
                    'field': 'energy',
                    'params': {
                        'axis': 0
                    }
                }
            ],
            ...
        }
    """
    kwargs = params or {}
    return data.cumsum(**kwargs)


def add(data, params=None):
    """
    Add function aggregation.

    Example config:

    .. code-block:: python

        config = {
            ...
            'fields': ['timestamp', 'x'],
            'aggregations': [
                {
                    'func': 'add',
                    'field': 'x',
                    'params': {
                        'by': 10
                    }
                }
            ],
            ...
        }
    """
    kwargs = params or {}
    constant = kwargs.get('by', 0)
    return data + constant


def subtract(data, params=None):
    """
    Subtract function aggregation.

    Example config:

    .. code-block:: python

        config = {
            ...
            'fields': ['timestamp', 'x'],
            'aggregations': [
                {
                    'func': 'subtract',
                    'field': 'x',
                    'params': {
                        'by': 10
                    }
                }
            ],
            ...
        }
    """
    kwargs = params or {}
    constant = kwargs.get('by', 0)
    return data - constant


def multiply(data, params=None):
    """
    Multiply function aggregation.

    Example config:

    .. code-block:: python

        config = {
            ...
            'fields': ['timestamp', 'x'],
            'aggregations': [
                {
                    'func': 'multiply',
                    'field': 'x',
                    'params': {
                        'by': 10
                    }
                }
            ],
            ...
        }
    """
    kwargs = params or {}
    factor = kwargs.get('by', 1.0)
    return data * factor


def divide(data, params=None):
    """
    Divide function aggregation.

    Example config:

    .. code-block:: python

        config = {
            ...
            'fields': ['timestamp', 'energy'],
            'aggregations': [
                {
                    'func': 'divide',
                    'field': 'energy',
                    'params': {
                        'by': 10
                    }
                }
            ],
            ...
        }
    """
    kwargs = params or {}
    factor = kwargs.get('by', 1.0)
    return data / factor


def power(data, params=None):
    """
    Power function aggregation.

    Example config:

    .. code-block:: python

        config = {
            ...
            'fields': ['timestamp', 'x'],
            'aggregations': [
                {
                    'func': 'power',
                    'field': 'x',
                    'params': {
                        'by': 2
                    }
                }
            ],
            ...
        }
    """
    kwargs = params or {}
    factor = kwargs.get('by', 1.0)
    return data ** factor


def merge_dataframe(entries, **kwargs):
    """
    Merge all Pandas DataFrame objects from list of entries.

    We use pandas.DataFrame.append function to append all entries. Each entry
    must be an instance of pandas.DataFrame object.
    """
    df = pd.DataFrame()
    for entry in entries:
        if entry is not None:
            if not isinstance(entry, pd.DataFrame):
                raise ChartError(
                    'Data type to merge must be an instance of '
                    'pandas.DataFrame object.')
            df = df.append(entry, **kwargs)
    return df
