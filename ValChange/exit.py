from os import remove
from pathlib import Path
from ValStorage import json_read, json_write, utilsPath

from .proc import kill_all
from .structs import ChangeUser
from .config import get_password
from .switch import restore_cookies
from .options import restore_options
from .launch import get_programs
from .switch import restore_cookies, images as riotImages
from .subproc import wait_threads

lockFile: Path = utilsPath / "change" / "lock"


def restore_all():
    data = json_read(lockFile)
    cUser = ChangeUser.from_dict(data)
    if cUser.isDefault:
        return
    get_password(cUser)
    restore_options(cUser)
    restore_cookies()


def lock(cUser: ChangeUser):
    cUser.user.password = ""
    data = cUser.to_dict()
    json_write(data, lockFile)


def unlock():
    lockFile.unlink(missing_ok=True)


def fault():
    if not lockFile.exists():
        return
    restore_all()
    unlock()


def clean_exit(cUser: ChangeUser):
    if not cUser.isDefault:
        restore_cookies()
    kill_all(riotImages)
    kill_all([p.path.name for p in get_programs().list if p.close])
    wait_threads()
    unlock()
