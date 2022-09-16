from sys import argv
from ValConfig.auth import getPass, init as init_auth
from ValConfig.storage import jsonRead, jsonWrite, settingsPath
from ValConfig.structs import User

from .structs import ChangeUser

def switcher_write(data,file):
	jsonWrite(data, settingsPath / "switcher" / file)

def switcher_read(file):
	return jsonRead(settingsPath / "switcher" / file)

def get_config():
	alias = switcher_read("alias.json")
	configFile = switcher_read("config.json")

	cfg = configFile["defaultConfig"]
	defaultUser = configFile["defaultUser"]
	pull = configFile["pullConfig"]

	username = alias[argv[1]]

	user = User(username, "")
	cUser = ChangeUser(user, defaultUser, cfg, pull)
	return cUser

def get_password(cUser: ChangeUser):
	init_auth()
	cUser.user.password = getPass(cUser.username)
