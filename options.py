from ValVault import get_auth, get_pass, User
from ValConfig.api import getPreference, setPreference
from ValConfig.config import config, configList
from ValConfig.loadout import loadout, loadList

from .structs import ChangeUser

def get_prefs(username):
	user = User(username, get_pass(username))
	auth = get_auth(user)
	prefs = getPreference(auth)
	return prefs

def set_prefs(user, data):
	auth = get_auth(user)
	setPreference(auth, data)

def pull_prefs(cUser: ChangeUser):
	prefs = get_prefs(cUser.defaultUser)
	config("backup", cUser.user, "")
	set_prefs(cUser.user, prefs)

def set_options(cUser: ChangeUser):
	if (cUser.pull):
		pull_prefs(cUser)
	elif (cUser.cfg in configList()):
		config("import", cUser.user, cUser.cfg)
	if (cUser.cfg in loadList(cUser.username)):
		loadout("import", cUser.user, cUser.cfg)

def restore_options(cUser: ChangeUser):
	if (cUser.cfg in configList() or cUser.pull):
		config("restore", cUser.user, "")
	if (cUser.cfg in loadList(cUser.username)):
		loadout("dump", cUser.user, cUser.cfg)
		loadout("restore", cUser.user, "")
