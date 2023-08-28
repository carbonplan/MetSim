import re

import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import date2num, num2date

DEFAULT_ORIGIN = '0001-01-01'


def date_range(start=None, end=None, periods=None, freq='D', tz=None,
               normalize=False, name=None, inclusive='both', calendar='standard',
               **kwargs,):
    ''' Return a fixed frequency datetime index, with day (calendar) as the
    default frequency

    Parameters
    ----------
    start : string or datetime-like, default None
        Left bound for generating dates
    end : string or datetime-like, default None
        Right bound for generating dates
    periods : integer or None, default None
        If None, must specify start and end
    freq : string or DateOffset, default 'D' (calendar daily)
        Frequency strings can have multiples, e.g. '5H'
    tz : string or None
        Time zone name for returning localized DatetimeIndex, for example
        Asia/Hong_Kong
    normalize : bool, default False
        Normalize start/end dates to midnight before generating date range
    name : str, default None
        Name of the resulting index
    closed : string or None, default None
        Make the interval closed with respect to the given frequency to
        the 'left', 'right', or both sides (None)
    calendar : string
        Describes the calendar used in the time calculations. Default is a the
        standard calendar (with leap years)

    Notes
    -----
    2 of start, end, or periods must be specified
    To learn more about the frequency strings, please see `this link
    <http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases>`__.

    Returns
    -------
    rng : DatetimeIndex
    '''
    return pd.date_range(
        start=start,
        end=end,
        periods=periods,
        freq=freq,
        tz=tz,
        normalize=normalize,
        name=name,
        inclusive=inclusive,
        **kwargs,
    )


def decode_freq(freq):
    if len(freq) > 1:
        r = re.compile('([0-9]+)([a-zA-Z]+)')
        step, unit = r.match(freq).groups()
    else:
        step = 1
        unit = freq
    return (int(step), units_from_freq(unit))


def units_from_freq(freq, origin=DEFAULT_ORIGIN):
    if 'H' in freq:
        return 'hours since %s' % origin
    elif 'D' in freq:
        return 'days since %s' % origin
    elif 'T' in freq:
        return 'minutes since %s' % origin
    else:
        raise NotImplementedError(
            'freq {} not supported at this time'.format(freq))
