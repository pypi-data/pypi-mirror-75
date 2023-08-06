"""
Pretty Color Log
"""

import os
from configparser import ConfigParser
from pkg_resources import resource_filename

from .formatters import CoreFormatter as Fmt


META: ConfigParser = ConfigParser()
META.read(resource_filename(__name__, os.path.join('conf', 'meta.ini')))

__author__: str = META['default']['author']
__version__: str = META['default']['version']
__email__: str = META['default']['email']
__url__: str = META['default']['url']
