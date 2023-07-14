from ValVault.terminal import get_pass, User
from ValLib.api import get_preference, set_preference
from ValConfig.config import (
    backup as backup_config,
    import_from_file as import_config,
    restore as restore_config,
    config_list
)
from ValConfig.loadout import (
    backup as backup_loadout,
    import_from_file as import_loadout,
    save_to_file as dump_loadout,
    restore as restore_loadout,
    load_list
)

from ..helper import get_auth, get_extra_auth
from ..structs import ChangeUser


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
    auth = get_auth(cUser.user)
    backup_config(cUser.user, auth)
    set_prefs(cUser.user, prefs)


def set_options(cUser: ChangeUser):
    if cUser.pull:
        pull_prefs(cUser)
    elif cUser.cfg in config_list():
        auth = get_auth(cUser.user)
        backup_config(cUser.user, auth)
        import_config(cUser.cfg, auth)
    if cUser.cfg in load_list(cUser.username):
        auth = get_extra_auth(cUser.user)
        backup_loadout(auth)
        import_loadout(cUser.cfg, auth)


def restore_options(cUser: ChangeUser):
    if cUser.cfg in config_list() or cUser.pull:
        auth = get_auth(cUser.user)
        restore_config(cUser.user, auth, -1)
    if cUser.cfg in load_list(cUser.username):
        auth = get_extra_auth(cUser.user)
        dump_loadout(cUser.cfg, auth)
        restore_loadout(auth)
