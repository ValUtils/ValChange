import yaml

from ValStorage import *


def read_yaml(file):
    with open(file, "r") as f:
        return yaml.load(f, yaml.Loader)


def write_yaml(file, data):
    with open(file, "w") as f:
        yaml.safe_dump(data, f, indent=4)


def set_path():
    global changePath
    utilsPath = utils_path()
    changePath = utilsPath / "change"
    create_path(changePath)


set_path()
