from ValManager import config, loadout
from ValLib.api import get_preference, set_preference
from ValVault.terminal import User, get_pass

from ..debug import Level, log
from ..structs import ChangeUser, Status
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
    config.backup(cUser.user, auth)
    set_prefs(cUser.user, prefs)


def set_options(cUser: ChangeUser):
    path = f"{cUser.defaultUser}.json"
    if cUser.pull:
        pull_prefs(cUser)
        cUser.restoreConfig = True
    elif cUser.cfg in config.list():
        auth = get_auth(cUser.user)
        config.backup(cUser.user, auth)
        config.upload(cUser.cfg, auth)
        cUser.restoreConfig = True
    if path in loadout.list(cUser.username):
        auth = get_extra_auth(cUser.user)
        loadout.backup(auth)
        loadout.upload(path, auth)
        cUser.restoreLoadout = True
    cUser.status = Status.CONFIG


def restore_options(cUser: ChangeUser):
    path = f"{cUser.defaultUser}.json"
    if cUser.restoreConfig:
        auth = get_auth(cUser.user)
        config.restore(cUser.user, auth, -1)
    if cUser.restoreLoadout:
        auth = get_extra_auth(cUser.user)
        loadout.download(path, auth)
        loadout.restore(auth)
