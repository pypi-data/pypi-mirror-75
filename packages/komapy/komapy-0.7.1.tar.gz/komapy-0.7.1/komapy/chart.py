"""
KomaPy Chart module.

KomaPy chart design philosophy is only use config to create customizable chart.
It wraps matplotlib axes object and provides BMA data fetching mechanism that
allow user to create customizable chart with ease and simplicity.

Example:

.. code-block:: python

    from komapy import Chart

    chart = Chart({
        'title': 'RB2',
        'theme': 'seaborn',
        'layout': {
            'data': [
                {
                    'series': {
                        'name': 'edm',
                        'query_params': {
                            'benchmark': 'BAB0',
                            'reflector': 'RB2',
                            'start_at': '2019-04-01',
                            'end_at': '2019-08-01',
                            'ci': True
                        },
                        'fields': ['timestamp', 'slope_distance'],
                        'xaxis_date': True
                    }
                }
            ]
        }
    })

    chart.render()
    chart.save('RB2.png')
"""

import copy
from collections import Callable
from functools import partial

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from . import addons, extensions, utils
from .axis import (
    build_secondary_axis,
    build_tertiary_axis,
    customize_axis,
    set_axis_formatter,
    set_axis_label,
    set_axis_legend,
    set_axis_locator,
)
from .cache import ResolverCache
from .constants import SUPPORTED_TYPES
from .exceptions import ChartError
from .layout import Layout
from .series import Series, addon_registers
from .settings import app_settings

register_matplotlib_converters()


def apply_theme(name):
    """Apply matplotlib plot theme."""
    if name in plt.style.available:
        plt.style.use(name)


class Chart(object):
    """A chart object."""

    def __init__(self, config):
        self.config = config

        self.title = config.get('title')
        self.theme = config.get('theme')
        self.legend = config.get('legend', {})
        self.timezone = config.get('timezone', app_settings.TIME_ZONE)

        config_layout = config.get('layout', {})
        self.layout = Layout(**config_layout)

        self.figure_options = config.get('figure_options', {})
        self.save_options = config.get('save_options', {})
        self.extensions = config.get('extensions', {})
        self.tight_layout = config.get('tight_layout', {})
        self.rc_params = config.get('rc_params', {})
        self.use_cache = config.get('use_cache', False)

        self.figure = None
        self.axes = []
        self.rendered_axes = []
        self.series = []
        self.data = []

        self._cache = {}
        self._plotted_axes = []
        self._validate()

    def get_config(self):
        """
        Get original chart config.
        """
        return self.config

    def get_series(self, index=None):
        """
        Get series instance.
        """
        if index is not None:
            if isinstance(index, int):
                if index > len(self.series):
                    raise ChartError('Index out of range')
                return self.series[index]
            else:
                for s in self.series:
                    if s.index == index:
                        return s
                return None
        return self.series

    def get_series_and_data(self, index=None):
        """
        Get series and data pair.
        """
        if index is not None:
            if isinstance(index, int):
                if index > len(self.data):
                    raise ChartError('Index out of range')
                return self.data[index]
            else:
                for (s, d) in self.data:
                    if s.index == index:
                        return (s, d)
                return None
        return self.data

    def get_data(self, index=None):
        """
        Get series data.
        """
        if index is not None:
            if isinstance(index, int):
                if index > len(self.data):
                    raise ChartError('Index out of range')
                return self.data[index][1]
            else:
                for (s, d) in self.data:
                    if s.index == index:
                        return d
                return None
        return [d for (s, d) in self.data]

    def _validate(self):
        self.layout.validate()

        for layout in self.layout.data:
            layout_series = layout.get('series')
            if isinstance(layout_series, list):
                for params in layout_series:
                    config = Series(**params)
                    config.validate()
            elif isinstance(layout_series, dict):
                params = layout_series
                config = Series(**params)
                config.validate()

    @property
    def num_subplots(self):
        """Get number of subplots."""
        return len(self.layout.data)

    def _fetch_resource(self, series, **kwargs):
        return series.fetch_resource(**kwargs)

    def _resolve_data(self, series, **kwargs):
        """
        Resolve series data. Return cached version if use_cache=True.
        """
        if self.use_cache:
            cache_key = ResolverCache.create_key_from_series(series)
            if cache_key in self._cache:
                data = self._cache[cache_key]
                plot_data = series.resolve_data(resource=data)
                return plot_data

            data = self._fetch_resource(series, **kwargs)
            plot_data = series.resolve_data(resource=data)
            self._cache[cache_key] = data
        else:
            data = self._fetch_resource(series, **kwargs)
            plot_data = series.resolve_data(resource=data)
        return plot_data

    def _build_addons(self, axis, addons_entry):
        for addon in addons_entry:
            if isinstance(addon, dict):
                name = addon.pop('name', None)
                if isinstance(name, str):
                    if name in addon_registers:
                        resolver = addon_registers[name]
                        if isinstance(resolver, str):
                            callback = getattr(addons, resolver)
                        elif isinstance(resolver, Callable):
                            callback = resolver
                        else:
                            raise ChartError(
                                'Addons resolver must be a string registered '
                                'in the addons global registry or a callable '
                                'function')
                        callback(axis, **addon)
                elif isinstance(name, Callable):
                    callback = name
                    callback(axis, **addon)
            elif isinstance(addon, Callable):
                callback = addon
                callback(axis)

    def _build_series(self, axis, params):
        series = Series(**params)
        self.series.append(series)

        if isinstance(series.fields, Callable):
            self.data.append((series, None))
            return series.fields(axis, **series.field_options)

        plot_data = self._resolve_data(series)
        self.data.append((series, plot_data))

        if series.axis:
            gca = self._plotted_axes[series.axis]
        else:
            if series.secondary:
                gca = build_secondary_axis(axis, on=series.secondary)
            elif series.tertiary.get('on'):
                gca = build_tertiary_axis(axis, **series.tertiary)
            else:
                gca = axis

        plot = getattr(gca, SUPPORTED_TYPES[series.type])
        partial(plot, *plot_data, **series.plot_params)()

        set_axis_label(gca, params=series.labels)
        locators = set_axis_locator(gca, params=series.locator)
        set_axis_formatter(gca, params=series.formatter, locators=locators)
        set_axis_legend(gca, series.legend)

        gca.set_title(series.title)
        customize_axis(axis, params)

        if series.addons:
            self._build_addons(gca, series.addons)

        return gca

    def _build_series_legend(self, axis, handles, labels, params=None):
        options = params or {}

        if options.pop('show', False):
            axis.legend(handles, labels, **options)

    def _build_layout(self, axis, layout):
        subplot_axes = []
        if not layout.get('series'):
            return subplot_axes

        subplot_handles = []
        subplot_labels = []
        if isinstance(layout['series'], list):
            for series_data in layout['series']:
                gca = self._build_series(axis, series_data)
                subplot_axes.append(gca)

                handle, label = gca.get_legend_handles_labels()
                for index, _ in enumerate(handle):
                    if handle[index] not in subplot_handles:
                        subplot_handles.append(handle[index])
                for index, _ in enumerate(label):
                    if label[index] not in subplot_labels:
                        subplot_labels.append(label[index])
                self._plotted_axes.append(gca)
        elif isinstance(layout['series'], dict):
            gca = self._build_series(axis, layout['series'])
            subplot_axes.append(gca)

            handle, label = gca.get_legend_handles_labels()
            subplot_handles += handle
            subplot_labels += label

        self._build_series_legend(
            gca, subplot_handles, subplot_labels, layout.get('legend', {}))

        return subplot_axes

    def _build_figure(self):
        self.figure = plt.figure(**self.figure_options)

    def _build_axes_rank(self):
        share = []
        for index in range(self.num_subplots):
            if self.layout.type == 'grid':
                options = self.layout.data[index]['grid'].get('options', {})
            else:
                options = self.layout.data[index].get('options', {})
            sharex = options.get('sharex', -1)
            share.append(sharex)
            sharey = options.get('sharey', -1)
            share.append(sharey)

        results = [(share.count(index), index)
                   for index in range(self.num_subplots)]

        return sorted(results, reverse=True)

    def _build_axes(self):
        keys = ['sharex', 'sharey']

        if self.layout.type == 'grid':
            layout_size = self.layout.size

            rank = self._build_axes_rank()
            for _, index in rank:
                grid = self.layout.data[index]['grid']
                location = grid['location']
                options = grid.get('options', {})

                for key in keys:
                    share_index = options.get(key)
                    if share_index:
                        options.update({key: self.axes[share_index]})
                self.axes[index] = plt.subplot2grid(
                    layout_size, location, **options)
        else:
            num_columns = 1
            options = self.layout.options
            if self.num_subplots == 0:
                num_rows = 1
            else:
                num_rows = self.num_subplots

            self.figure, self.axes = plt.subplots(
                num_rows, num_columns, **options)

    def _build_extension_series(self, axis, starttime, endtime):
        if not starttime:
            raise ChartError(
                'Parameter starttime is required to build extension series')
        if not endtime:
            raise ChartError(
                'Parameter endtime is required to build extension series')

        handles = []
        labels = []
        plot = copy.deepcopy(self.extensions.get('plot', []))

        for item in plot:
            name = item.pop('name', None)
            if name is None:
                continue

            if isinstance(name, Callable):
                method = name
                labels.append(item.pop('label', ''))
                handle = method(axis, starttime, endtime, **item)
            else:
                if name not in extensions.extension_registers:
                    continue
                resolver = extensions.extension_registers[name]['resolver']
                if isinstance(resolver, Callable):
                    method = resolver
                elif isinstance(resolver, str):
                    method = getattr(
                        extensions,
                        extensions.extension_registers[name]['resolver'])

                labels.append(item.pop(
                    'label',
                    extensions.extension_registers[name].get('label', '')))
                handle = method(axis, starttime, endtime, **item)

                if handle:
                    handles.append(handle)
                else:
                    labels.pop()

        return handles, labels

    def _build_extension_plot(self, axis):
        if self.extensions:
            starttime = utils.to_pydatetime(
                self.extensions['starttime'],
                timezone=self.timezone
            ) if self.extensions.get('starttime') else None

            endtime = utils.to_pydatetime(
                self.extensions['endtime'],
                timezone=self.timezone
            ) if self.extensions.get('endtime') else None

            handles, labels = self._build_extension_series(
                axis, starttime, endtime)
            legend = self.extensions.pop('legend', {})

            if legend:
                show = legend.pop('show', False)
                if show:
                    self.figure.legend(handles, labels, **legend)

    def _update_rc_params(self):
        plt.rcParams.update(self.rc_params)

    def render(self):
        """
        Render chart object.

        It builds figure, layout, series, fetchs resource from data sources,
        renders matplotlib axes objects, and performs other tasks.
        """

        self._update_rc_params()
        apply_theme(self.theme)

        self.axes = [None] * self.num_subplots
        self.rendered_axes = []

        self._build_figure()
        self._build_axes()

        if self.num_subplots < 2:
            self.axes = [self.axes]

        for axis, layout in zip(self.axes, self.layout.data):
            subplot_axes = self._build_layout(axis, layout)
            self.rendered_axes.append(subplot_axes)
            self._build_extension_plot(axis)

    def save(self, filename):
        """Export chart object to file."""

        if self.num_subplots > 1:
            self.figure.suptitle(self.title)
        else:
            plt.title(self.title)

        if self.tight_layout:
            plt.tight_layout(**self.tight_layout)
        plt.savefig(filename, **self.save_options)

    def clear(self):
        """Clear all chart axes and figures."""

        if self.figure:
            plt.close(self.figure)

        plt.clf()
        plt.close('all')

    def cache_clear(self):
        """
        Clear all chart caches.
        """
        self._cache.clear()
