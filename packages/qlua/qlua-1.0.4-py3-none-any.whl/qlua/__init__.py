"""
Quik Lua RPC API.
"""

from os.path import join
from pkg_resources import resource_filename
from configparser import ConfigParser
from . import rpc
from .rpc import *


META = ConfigParser()
META.read(resource_filename(__name__, join('conf', 'meta.ini')))

__author__ = META['default']['author']
__version__ = META['default']['version']
__email__ = META['default']['email']
__url__ = META['default']['url']

__all__ = rpc.__all__

for i in [join, resource_filename, ConfigParser]:
    del globals()[i.__name__]
