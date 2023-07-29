from typing import Dict
from ValVault.terminal import get_auth
from ValLib.api import get_region
from ValLib import User, ExtraAuth

_regions: Dict[User, str] = {}


def get_extra_auth(user: User, reauth=False):
    auth = get_auth(user, reauth=reauth)
    if user not in _regions:
        _regions[user] = get_region(auth)
    return ExtraAuth(user.username, _regions[user], auth)
