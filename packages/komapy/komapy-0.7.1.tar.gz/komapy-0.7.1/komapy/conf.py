import json

from .settings import app_settings

_cached_attrs = {}


class Settings:
    """
    A proxy to get or set app settings.
    """

    def __getattr__(self, attr):
        if attr in _cached_attrs:
            return _cached_attrs[attr]
        return getattr(app_settings, attr, None)

    def __setattr__(self, attr, value):
        if hasattr(app_settings, attr):
            setattr(app_settings, attr, value)
        _cached_attrs[attr] = value

    def from_dict(self, settings):
        """
        Set settings from dictionary object.
        """
        for attr, value in settings.items():
            setattr(self, attr, value)

    def from_json(self, settings):
        """
        Set settings from JSON object.
        """
        dict_settings = json.loads(settings)
        self.from_dict(dict_settings)

    def from_json_file(self, path):
        """
        Set settings from JSON file.
        """
        with open(path) as fp:
            dict_settings = json.load(fp)
        self.from_dict(dict_settings)

    def as_dict(self):
        """
        Export all settings as dictionary object.
        """
        dict_settings = {}
        for key, value in _cached_attrs.items():
            dict_settings[key] = value

        for key in app_settings.defaults:
            dict_settings.update({key: getattr(app_settings, key)})

        return dict_settings


settings = Settings()
