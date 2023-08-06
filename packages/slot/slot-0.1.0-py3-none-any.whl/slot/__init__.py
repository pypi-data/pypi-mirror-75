from importlib_metadata import version
from os import makedirs

from .constants import STORES_DIR

makedirs(STORES_DIR, exist_ok=True)

__version__ = version('slot')
