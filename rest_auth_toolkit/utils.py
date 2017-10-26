from django.conf import settings
from django.utils.module_loading import import_string


# TODO follow drf's pattern of having all default setting values in one place


class MissingSetting(Exception):
    """Exception raised by get_setting and get_object_from_setting."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'setting REST_AUTH_TOOLKIT[{!r}] not found'.format(self.name)


_NotGiven = object()


def get_setting(name, default=_NotGiven):
    """Find setting in REST_AUTH_TOOLKIT dict.

    Return default is not found, or raise MissingSetting if no default.
    """
    config = getattr(settings, 'REST_AUTH_TOOLKIT', {})
    if name in config:
        return config[name]
    elif default is not _NotGiven:
        return default
    else:
        raise MissingSetting(name)


def get_object_from_setting(name, default=_NotGiven):
    """Find and import a dotted path settting.

    default should be the real object, not a dotted path.
    MissingSetting is raised if setting is not found and there
    is no default.
    """
    value = get_setting(name, default)
    if value is default:
        return default
    else:
        return import_string(value)
