import os


ROOT_DIR = os.path.expanduser(os.environ.get('SLOT_DATA_DIR', '~/.slot'))
STORES_DIR = os.path.join(ROOT_DIR, 'stores')
