from sys import argv
from ValVault.terminal import get_pass, get_name, init_vault, User

from .structs import ChangeUser, Settings
from .storage import get_settings, changePath


def get_username(settings: Settings):
    if len(argv) <= 1:
        return settings.defaultUser
    init_vault()
    alias = argv[1]
    return get_name(alias)


def get_config(name=""):
    settings = get_settings(Settings, changePath / "config.json")
    username = get_username(settings)
    user = User(name or username, "")
    cUser = ChangeUser(user, settings)
    return cUser


def get_password(cUser: ChangeUser):
    init_vault()
    cUser.user.password = get_pass(cUser.username)
