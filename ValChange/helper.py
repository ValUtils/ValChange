from time import time
from typing import Dict
from ValLib import authenticate, User, ExtraAuth, Auth
from ValLib.api import get_region
from ValLib.riot import cookie_token

_users: Dict[User, Auth] = {}
_extra: Dict[User, ExtraAuth] = {}


ONE_DAY = 86400.0


def has_expired(user: User):
    return time() > _users[user].expire


def cookies_expired(auth: Auth):
    return ONE_DAY * 30 > (auth.created - time())


def best_auth(user: User, auth: Auth):
    if auth.remember and not cookies_expired(auth):
        token, cookies = cookie_token(auth.cookies)
        auth.token = token
        auth.cookies = cookies
        return auth
    return authenticate(user, auth.remember)


def get_auth(user: User, remember=False, reauth=False):
    if user not in _users:
        auth = authenticate(user, remember)
        _users[user] = auth
        return auth

    if reauth or has_expired(user):
        auth = best_auth(user, _users[user])
        _users[user] = auth
        return auth

    return _users[user]


def get_extra_auth(user: User, reauth=False):
    if reauth or user not in _extra:
        auth = get_auth(user, reauth=reauth)
        region = get_region(auth)
        _extra[user] = ExtraAuth(user.username, region, auth)

    return _extra[user]
