import requests
from ValConfig.riot import setupSession, setupAuth
from ValConfig.structs import User


def getCookies(session: requests.Session, user: User):
	data = {
		'type': 'auth',
		'remember': True,
		'username': user.username,
		'password': user.password
	}

	r = session.put(f'https://auth.riotgames.com/api/v1/authorization', json=data)
	if ("error" in data):
		raise BaseException(data['error'])
	
	cookies = r.cookies.get_dict()
	return cookies


def clientAuth(user: User):
	session = setupSession()
	setupAuth(session)
	return getCookies(session, user)