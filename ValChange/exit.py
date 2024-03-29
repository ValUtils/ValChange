from pathlib import Path

from .config import get_password
from .debug import Level, log
from .locale import unlink
from .ps import (
    exit_programs,
    get_programs,
    kill_all,
    process_exists,
    wait_threads
)
from .riot import restore_options
from .storage import json_read, lockFile
from .structs import ChangeUser, Status
from .switch import images as riotImages, restore_cookies


def restore_all():
    data = json_read(lockFile)
    cUser = ChangeUser.from_dict(data)
    if cUser.isDefault:
        return
    if cUser.status.in_range(Status.CONFIG, Status.CLEANED):
        get_password(cUser)
        restore_options(cUser)
    if cUser.status.in_range(Status.COOKIES, Status.COOKIES_RESTORED):
        restore_cookies()


def unlock():
    lockFile.unlink(missing_ok=True)


def fault():
    if not lockFile.exists():
        return
    log(Level.INFO, "Restoring lockfile")
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
    log(Level.INFO, "Exiting per user command")
    started = process_exists("VALORANT-Win64-Shipping.exe")
    kill_all(riotImages)
    restore_cookies()
    wait(started)
    unlock()
