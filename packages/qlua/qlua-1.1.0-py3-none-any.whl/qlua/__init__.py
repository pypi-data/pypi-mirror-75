"""
Пакет для работы с Quik LUA RPC.
"""

from os.path import join
from configparser import ConfigParser
from pkg_resources import resource_filename


META = ConfigParser()
META.read(resource_filename(__name__, join('conf', 'meta.ini')))

__author__ = META['default']['author']
__version__ = META['default']['version']
__email__ = META['default']['email']
__url__ = META['default']['url']
