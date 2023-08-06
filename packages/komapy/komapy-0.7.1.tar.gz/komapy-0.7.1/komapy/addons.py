import copy

from .constants import get_phase_dates
from .exceptions import ChartError
from .utils import compute_middletime, time_to_offset, to_pydatetime

addon_registers = {
    'komapy.addons.plot_activity_phases': 'plot_activity_phases',
    'komapy.addons.set_axis_xlimit': 'set_axis_xlimit',
    'komapy.addons.set_axis_ylimit': 'set_axis_ylimit',
}


def set_axis_xlimit(axis, **options):
    """
    Set the x-axis view limits. Set ``value`` in add-on entry parameters to
    particular minimum and maximum value. Set additional ``datetime`` to true
    if the axis is using date time value.

    Example:

    .. code-block:: python

        from komapy.series import Series

        series = Series(
            addons=[
                {
                    'name': 'xlimit',
                    'value': ['2019-04-01', '2019-08-01'],
                    'datetime': True,
                }
            ]
        )
    """
    value = options.get('value')
    if not value:
        raise ChartError(
            'Parameter value is required if xlimit add-ons is enabled')
    if len(value) < 2:
        raise ChartError('Unsufficient parameter value length')

    timezone = options.get('timezone')
    if options.get('datetime'):
        x1 = to_pydatetime(value[0], timezone=timezone)
        x2 = to_pydatetime(value[1], timezone=timezone)
    axis.set_xlim(x1, x2)


def set_axis_ylimit(axis, **options):
    """
    Set the y-axis view limits. Set ``value`` in add-on entry parameters to
    particular minimum and maximum value. Set additional ``datetime`` to true
    if the axis is using date time value.

    Example:

    .. code-block:: python

        from komapy.series import Series

        series = Series(
            addons=[
                {
                    'name': 'ylimit',
                    'value': ['2019-04-01', '2019-08-01'],
                    'datetime': True,
                }
            ]
        )
    """
    value = options.get('value')
    if not value:
        raise ChartError(
            'Parameter value is required if ylimit add-ons is enabled')
    if len(value) < 2:
        raise ChartError('Unsufficient parameter value length')

    timezone = options.get('timezone')
    if options.get('datetime'):
        y1 = to_pydatetime(value[0], timezone=timezone)
        y2 = to_pydatetime(value[1], timezone=timezone)
    axis.set_ylim(y1, y2)


def filter_date_in_range(phase_dates, starttime, endtime):
    """
    Exclude phases date outside range, and handle its date boundary.
    """
    phases = copy.deepcopy(phase_dates)
    for item in phases:
        if not (item[0] >= starttime and item[0] < endtime):
            item[0] = None
        if not (item[1] > starttime and item[1] <= endtime):
            item[1] = None

    new_phases = [
        item for item in phases if not (item[0] is None and item[1] is None)
    ]
    new_phases[0][0] = starttime
    new_phases[-1][1] = endtime
    return new_phases


def calculate_middle_date(phase_dates):
    """
    Calculate middle time from phase dates entry.
    """
    phases = []
    for item in phase_dates:
        phases.append([compute_middletime(item[0], item[1]), item[2]])
    return phases


def plot_activity_phases(axis, **options):
    """
    Plot activity phases labels on current axis.

    Note that this function requires 'starttime' and 'endtime' to be set on the
    series options to determine which labels to render in the plot figure.

    Phase text can be overrided by providing labels on series options.
    """

    def get_value_or_none(data, index):
        try:
            return data[index]
        except IndexError:
            return None

    default_offset_value = 1.1
    labels = options.pop('labels', [])
    starttime = to_pydatetime(options.pop('starttime')).replace(tzinfo=None)
    endtime = to_pydatetime(options.pop('endtime')).replace(tzinfo=None)

    PHASE_DATES = get_phase_dates()
    phase_dates = filter_date_in_range(PHASE_DATES, starttime, endtime)
    middle_time = calculate_middle_date(phase_dates)

    offsets = [
        [
            time_to_offset(starttime, endtime, item[0]),
            get_value_or_none(labels, index) or item[1]
        ] for index, item in enumerate(middle_time)
    ]
    offset = options.pop('offset', default_offset_value)
    for item in offsets:
        axis.text(item[0],
                  offset,
                  item[1],
                  horizontalalignment='center',
                  verticalalignment='center',
                  transform=axis.transAxes, **options)
