from typing import Dict

from ValLib import ExtraAuth, User
from ValLib.api import get_region, get_shard
from ValVault.terminal import get_auth

from ..debug import Level, log

_regions: Dict[User, str] = {}


def get_extra_auth(user: User, reauth=False):
    log(Level.DEBUG, f"Getting extra auth for {user.username}", "riot")
    auth = get_auth(user, reauth=reauth)
    if user not in _regions:
        _regions[user] = get_region(auth)
    region =  _regions[user]
    return ExtraAuth(user.username, region, get_shard(region), auth)
