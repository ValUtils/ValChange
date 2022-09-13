from sys import argv
from ValConfig.auth import getPass
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

	passwd = getPass(username)
	user = User(username, passwd)
	cUser = ChangeUser(user, defaultUser, cfg, pull)
	return cUser