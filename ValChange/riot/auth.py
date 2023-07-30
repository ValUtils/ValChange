from typing import Dict

from ValLib import ExtraAuth, User
from ValLib.api import get_region
from ValVault.terminal import get_auth

_regions: Dict[User, str] = {}


def get_extra_auth(user: User, reauth=False):
    auth = get_auth(user, reauth=reauth)
    if user not in _regions:
        _regions[user] = get_region(auth)
    return ExtraAuth(user.username, _regions[user], auth)
