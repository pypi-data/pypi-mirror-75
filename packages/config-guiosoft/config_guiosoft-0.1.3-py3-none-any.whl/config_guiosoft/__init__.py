__version__ = "0.1.3"
__description__ = "Guiosoft Python Configuration Class"
__author_name__ = "Guionardo Furlan"
__author_email__ = "guionardo@gmail.com"
__package_name__ = 'config_guiosoft'

__all__ = ['ConfigClass', 'ConfigType', 'DefaultValue']


from .config_class import ConfigClass
from .config_type import ConfigType
from .default_value import DefaultValue
