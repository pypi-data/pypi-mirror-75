import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test.signals import setting_changed


USER_SETTINGS = getattr(settings, "EMAIL_TOOLS", {})

DEFAULTS = {
    "FROM_EMAIL": None,
    "TEMPLATE_DIRECTORY": os.path.join(settings.BASE_DIR, "templates", "emails"),
}


class EmailSettings(object):
    """
    Based on https://github.com/encode/django-rest-framework/blob/master/rest_framework/settings.py
    """

    def __init__(self, settings=None, defaults=None):
        self.settings = settings or {}
        self.defaults = defaults or {}
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise ImproperlyConfigured(f"Invalid Email Tools setting: {attr}")

        try:
            val = self.settings[attr]
        except KeyError:
            val = self.defaults[attr]

        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()


email_settings = EmailSettings(USER_SETTINGS, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "EMAIL_TOOLS":
        email_settings.reload()


setting_changed.connect(reload_api_settings)
