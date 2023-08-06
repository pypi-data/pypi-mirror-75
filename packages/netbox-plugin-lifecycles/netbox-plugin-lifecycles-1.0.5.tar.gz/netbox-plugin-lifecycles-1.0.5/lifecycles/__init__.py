from extras.plugins import PluginConfig

class LifecyclesConfig(PluginConfig):
    name = 'lifecycles'
    verbose_name = 'lyfecycles'
    description = 'Lifecycles for devices'
    version = '1.0.5'
    author = 'DCIM'
    author_email = 'dcim@selectel.ru'
    base_url = 'lifecycles'
    required_settings = []
    default_settings = {
        'loud': False
    }

config = LifecyclesConfig
