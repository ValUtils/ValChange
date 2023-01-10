from os import remove
from pathlib import Path
from ValLib import User
from ValLib.storage import read_from_drive, save_to_drive, utilsPath

from .proc import kill_all
from .structs import ChangeUser
from .config import get_password
from .switch import restore_cookies
from .options import restore_options
from .launch import get_programs
from .switch import restore_cookies, images as riotImages

lockFile: Path = utilsPath / "change" / "lock"

def restore_all():
	data = read_from_drive(lockFile).split("||")
	user = User(data[0], "")
	cUser = ChangeUser(user, data[1], data[2], bool(int(data[3])))
	if (cUser.isDefault):
		return
	get_password(cUser)
	restore_options(cUser)
	restore_cookies()


def lock(cUser: ChangeUser):
	data = f"{cUser.username}||{cUser.defaultUser}||{cUser.cfg}||{int(cUser.pull)}"
	save_to_drive(data, lockFile)

def unlock():
	if (not lockFile.exists()):
		return
	remove(lockFile)

def fault():
	if (not lockFile.exists()):
		return
	restore_all()
	unlock()

def clean_exit(cUser: ChangeUser):
	if (not cUser.isDefault):
		restore_cookies()
	kill_all(riotImages)
	kill_all([p.path.name for p in get_programs().list])
	unlock()
