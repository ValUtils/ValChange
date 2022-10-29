import requests
from ValVault import User
from ValVault.riot import setup_session, setup_auth


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
	session = setup_session()
	setup_auth(session)
	return getCookies(session, user)