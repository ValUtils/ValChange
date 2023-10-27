from ValConfig.config import (
    backup as backup_config,
    config_list,
    import_from_file as import_config,
    restore as restore_config
)
from ValConfig.loadout import (
    backup as backup_loadout,
    import_from_file as import_loadout,
    load_list,
    restore as restore_loadout,
    save_to_file as dump_loadout
)
from ValLib.api import get_preference, set_preference
from ValVault.terminal import User, get_pass

from ..debug import Level, log
from ..structs import ChangeUser
from .auth import get_auth, get_extra_auth


def get_prefs(username):
    log(Level.DEBUG, f"Getting preferences for {username}", "riot")
    user = User(username, get_pass(username))
    auth = get_auth(user)
    prefs = get_preference(auth)
    return prefs


def set_prefs(user, data):
    log(Level.DEBUG, f"Setting preferences for {user.username}", "riot")
    auth = get_auth(user)
    set_preference(auth, data)


def pull_prefs(cUser: ChangeUser):
    log(Level.DEBUG,
        f"Pulling prefs from {cUser.defaultUser} to {cUser.username}", "riot")
    prefs = get_prefs(cUser.defaultUser)
    auth = get_auth(cUser.user)
    backup_config(cUser.user, auth)
    set_prefs(cUser.user, prefs)


def set_options(cUser: ChangeUser):
    path = f"{cUser.defaultUser}.json"
    if cUser.pull:
        pull_prefs(cUser)
    elif cUser.cfg in config_list():
        auth = get_auth(cUser.user)
        backup_config(cUser.user, auth)
        import_config(cUser.cfg, auth)
    if path in load_list(cUser.username):
        auth = get_extra_auth(cUser.user)
        backup_loadout(auth)
        import_loadout(path, auth)


def restore_options(cUser: ChangeUser):
    path = f"{cUser.defaultUser}.json"
    if cUser.cfg in config_list() or cUser.pull:
        auth = get_auth(cUser.user)
        restore_config(cUser.user, auth, -1)
    if path in load_list(cUser.username):
        auth = get_extra_auth(cUser.user)
        dump_loadout(path, auth)
        restore_loadout(auth)
