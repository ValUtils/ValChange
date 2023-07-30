from pathlib import Path

from .config import get_password
from .locale import unlink
from .proc import kill_all, process_exists
from .programs import exit_programs, get_programs
from .riot import restore_options
from .storage import changePath, json_read, json_write
from .structs import ChangeUser
from .subproc import wait_threads
from .switch import images as riotImages, restore_cookies

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
    exit_programs(get_programs())


def clean_exit():
    started = process_exists("VALORANT-Win64-Shipping.exe")
    kill_all(riotImages)
    restore_cookies()
    wait(started)
    unlock()
