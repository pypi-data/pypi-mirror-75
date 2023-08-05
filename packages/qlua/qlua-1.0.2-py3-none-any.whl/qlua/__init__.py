"""
Quik Lua RPC API.
"""

from .rpc import *


def META():
    """Package metadata."""
    from os.path import join
    from pkg_resources import resource_filename
    from configparser import ConfigParser

    meta = ConfigParser()
    meta.read(resource_filename(__name__, join('conf', 'meta.ini')))
    return meta['default']


META = META()
__author__ = META['author']
__version__ = META['version']
__email__ = META['email']
__url__ = META['url']
