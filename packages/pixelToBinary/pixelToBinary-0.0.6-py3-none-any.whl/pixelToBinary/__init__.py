# turn off warnings - interesting for development, but not for runtime
import warnings
import logging

from os.path import join

try:
    from .version import version as __version__
except ImportError:
    __version__ = "Version number is not available"

from . import image
from image import Bimage
from .utils import __pkg_dir__

__data_dir__ = join(__pkg_dir__, "data")
