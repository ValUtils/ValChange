from pathlib import Path

from .proc import kill_all, process_exists
from .structs import ChangeUser
from .config import get_password
from .switch import restore_cookies
from .riot import restore_options
from .launch import get_programs
from .switch import restore_cookies, images as riotImages
from .subproc import wait_threads
from .locale import unlink
from .storage import json_read, json_write, changePath

lockFile: Path = changePath / "lock"


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
    unlink()


def wait(started: bool):
    if started:
        wait_threads()
        return
    unlink()
    kill_all([p.path.name for p in get_programs().list if p.close])


def clean_exit():
    started = process_exists("VALORANT-Win64-Shipping.exe")
    kill_all(riotImages)
    restore_cookies()
    wait(started)
    unlock()
