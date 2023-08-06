import os
from glob import glob
from shutil import move

from use_dir import use_dir
from box import Box

from .constants import STORES_DIR
from .config import Config
from .exceptions import NotRegisteredError, InvalidOptionError


class Store:
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(STORES_DIR, name)

        config = Config()
        if name in config.stores.keys():
            self.target = config.stores[name].target

    @property
    def options(self):
        with use_dir(self.path):
            return glob('*')

    @property
    def registered(self):
        return self.exists and os.path.exists(self.target) and os.path.islink(self.target)

    @property
    def exists(self):
        return os.path.exists(self.path) and self.name in Config().stores.keys()

    @property
    def selected_option(self):
        return os.path.basename(os.readlink(self.target))

    def select(self, option):
        if not self.registered:
            raise NotRegisteredError(f'{self.name} is not registered')

        if option not in self.options:
            raise InvalidOptionError()

        os.unlink(self.target)
        os.symlink(os.path.join(self.path, option), self.target)

    def ingest(self, new_name, file_name=None, link=False):
        target = self.target

        if file_name is not None:
            target = file_name

        new_path = os.path.join(self.path, new_name)
        move(target, new_path)

        if link:
            os.symlink(new_path, self.target)

    def create(self, target):
        config = Config()

        os.makedirs(self.path, exist_ok=True)
        config.stores[self.name] = Box({})
        config.stores[self.name].target = target

        self.target = target

        Config.dump(config)
