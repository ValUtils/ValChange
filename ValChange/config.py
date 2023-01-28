from sys import argv
from ValVault import get_pass, get_name, init_vault, User
from ValStorage import json_read, json_write, utilsPath

from .structs import ChangeUser


def switcher_write(data, file):
    json_write(data, utilsPath / "change" / file)


def switcher_read(file):
    return json_read(utilsPath / "change" / file)


def get_username(config):
    if (len(argv) <= 1):
        return config["defaultUser"]
    init_vault()
    alias = argv[1]
    return get_name(alias)


def get_config(name=""):
    configFile = switcher_read("config.json")

    cfg = configFile["defaultConfig"]
    defaultUser = configFile["defaultUser"]
    pull = configFile["pullConfig"]

    username = get_username(configFile)

    user = User(name or username, "")
    cUser = ChangeUser(user, defaultUser, cfg, pull)
    return cUser


def get_password(cUser: ChangeUser):
    init_vault()
    cUser.user.password = get_pass(cUser.username)
