"""
KomaPy app settings.
"""

from .constants import TIME_ZONE

defaults = {
    'BMA_ACCESS_TOKEN': '',
    'BMA_API_CLASS': None,
    'BMA_API_HOST': '',
    'BMA_API_KEY': '',
    'BMA_API_PROTOCOL': '',
    'IGNORE_BMA_REQUEST_CACHE': False,
    'TIME_ZONE': TIME_ZONE,
}


class AppSettings:
    """
    A settings object. It defines access to the BMA API using API key or
    access token and other setting parameters.
    """

    def __init__(self, defaults=None):
        self.defaults = defaults or {}

        for attr, value in self.defaults.items():
            setattr(self, attr, value)


app_settings = AppSettings(defaults)
