import os
import importlib

ENVIRONMENT_VARIABLE = 'TEST_ENV'
DEFAULT_ENV = 'production'

def set_env():
    env = os.environ.get('TEST_ENV')
    return DEFAULT_ENV if env == None else env

def set_package():
    return __package__

class Settings:
    def __init__(self, settings_module):
        self.SETTINGS_MODULE = settings_module

        #try:
        mod = importlib.import_module(self.SETTINGS_MODULE)
        # except ModuleNotFoundError:
            # mod = importlib.import_module("settings." + set_env(), __package__)

        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }

settings_module = 'settings.' + set_env()
settings = Settings(settings_module)
