from sys import argv
from ValVault import get_pass, init as init_auth, User
from ValConfig.storage import json_read, json_write, settingsPath

from .structs import ChangeUser

def switcher_write(data,file):
	json_write(data, settingsPath / "switcher" / file)

def switcher_read(file):
	return json_read(settingsPath / "switcher" / file)

def get_username(config):
	alias = switcher_read("alias.json")
	if (len(argv) < 1):
		return config["defaultUser"]
	name = argv[1]
	if (name in alias):
		return alias[name]
	return name

def get_config():
	configFile = switcher_read("config.json")

	cfg = configFile["defaultConfig"]
	defaultUser = configFile["defaultUser"]
	pull = configFile["pullConfig"]

	username = get_username(configFile)

	user = User(username, "")
	cUser = ChangeUser(user, defaultUser, cfg, pull)
	return cUser

def get_password(cUser: ChangeUser):
	init_auth()
	cUser.user.password = get_pass(cUser.username)
