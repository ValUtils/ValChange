from sys import argv
from ValVault import get_pass, get_name, init_vault, User
from ValStorage import get_settings, json_read, json_write, utilsPath

from .structs import ChangeUser, Settings


def switcher_write(data, file):
    json_write(data, utilsPath / "change" / file)


def switcher_read(file):
    return json_read(utilsPath / "change" / file)


def get_username(settings: Settings):
    if (len(argv) <= 1):
        return settings.defaultUser
    init_vault()
    alias = argv[1]
    return get_name(alias)


def get_config(name=""):
    settings = get_settings(Settings, utilsPath / "change" / "config.json")
    username = get_username(settings)
    user = User(name or username, "")
    cUser = ChangeUser(user, settings)
    return cUser


def get_password(cUser: ChangeUser):
    init_vault()
    cUser.user.password = get_pass(cUser.username)
