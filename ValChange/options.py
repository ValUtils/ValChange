from ValVault.terminal import get_auth, get_pass, User
from ValLib.api import get_preference, set_preference
from ValConfig.config import config, config_list
from ValConfig.loadout import loadout, load_list

from .structs import ChangeUser


def get_prefs(username):
    user = User(username, get_pass(username))
    auth = get_auth(user)
    prefs = get_preference(auth)
    return prefs


def set_prefs(user, data):
    auth = get_auth(user)
    set_preference(auth, data)


def pull_prefs(cUser: ChangeUser):
    prefs = get_prefs(cUser.defaultUser)
    config("backup", cUser.user, "")
    set_prefs(cUser.user, prefs)


def set_options(cUser: ChangeUser):
    if cUser.pull:
        pull_prefs(cUser)
    elif cUser.cfg in config_list():
        config("import", cUser.user, cUser.cfg)
    if cUser.cfg in load_list(cUser.username):
        loadout("import", cUser.user, cUser.cfg)


def restore_options(cUser: ChangeUser):
    if cUser.cfg in config_list() or cUser.pull:
        config("restore", cUser.user, -1)
    if cUser.cfg in load_list(cUser.username):
        loadout("dump", cUser.user, cUser.cfg)
        loadout("restore", cUser.user, "")
