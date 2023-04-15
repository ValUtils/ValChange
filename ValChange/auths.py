import requests
from ValLib import User
from ValLib.riot import setup_session, setup_auth


def get_cookies(session: requests.Session, user: User):
    data = {
        'type': 'auth',
        'remember': True,
        'username': user.username,
        'password': user.password
    }

    r = session.put(
        f'https://auth.riotgames.com/api/v1/authorization', json=data)
    if "error" in data:
        raise BaseException(data['error'])

    cookies = r.cookies.get_dict()
    return cookies


def client_auth(user: User):
    session = setup_session()
    setup_auth(session)
    return get_cookies(session, user)
