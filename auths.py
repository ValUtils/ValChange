import requests
from ValVault import User
from ValVault.riot import setupSession, setupAuth


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