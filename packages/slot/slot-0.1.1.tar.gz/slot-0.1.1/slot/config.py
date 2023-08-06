import os

from box import Box
from ruamel.yaml import YAML

from .constants import ROOT_DIR


yaml = YAML(typ="safe")
yaml.default_flow_style = False

file_name = 'config.yml'


class Config:
    file_path = os.path.join(ROOT_DIR, file_name)

    def __new__(self, initial_data={}):
        try:
            return Config.load()
        except FileNotFoundError:
            pass

        data = {'stores': {}}
        data.update(initial_data)
        Config.dump(Box(data))

        return Config.load()

    @classmethod
    def load(cls):
        with open(cls.file_path) as f:
            return Box(yaml.load(f.read()))

    @classmethod
    def dump(cls, data):
        with open(cls.file_path, 'w') as f:
            yaml.dump(data.to_dict(), f)
