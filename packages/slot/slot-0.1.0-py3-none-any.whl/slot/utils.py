from glob import glob

from use_dir import use_dir

from .store import Store
from .constants import STORES_DIR


def get_all_stores():
    with use_dir(STORES_DIR):
        return [Store(d) for d in glob('*')]
