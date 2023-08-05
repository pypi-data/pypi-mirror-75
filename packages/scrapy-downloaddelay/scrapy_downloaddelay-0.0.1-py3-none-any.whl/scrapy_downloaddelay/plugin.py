from scrapy.settings import Settings
from distutils.util import strtobool

class Plugin:
    settings = None

    def perform(self, setting:Settings, plugin_settings):
        if not get_bool(plugin_settings.get('ENABLED', 'false')):
            return
        
        download_delay = plugin_settings.get('DOWNLOAD_DELAY')
        if download_delay:
            setting.set('DOWNLOAD_DELAY', download_delay)
            return
        
        download_delay_minimum = float(plugin_settings.get('DOWNLOAD_DELAY_MIN', 0))
        if download_delay_minimum > 0 and setting.getfloat('DOWNLOAD_DELAY') < download_delay_minimum:
            setting.set('DOWNLOAD_DELAY', download_delay_minimum)
            return
            
    def apply(self, settings, **kwargs):
        plugin_settings = self.settings or {}
        self.perform(settings, plugin_settings)


def get_bool(value):
    try:
        return bool(int(value))
    except ValueError:
        if value in ("True", "true"):
            return True
        if value in ("False", "false"):
            return False
        raise ValueError("Supported values for boolean settings "
                         "are 0/1, True/False, '0'/'1', "
                         "'True'/'False' and 'true'/'false'")