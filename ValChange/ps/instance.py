from sys import exit

from win32api import GetLastError
from win32event import CreateMutex
from winerror import ERROR_ALREADY_EXISTS


def already_running():
    _ = CreateMutex(None, 1, "org.valutils.valchange")  # type: ignore

    return GetLastError() == ERROR_ALREADY_EXISTS


def exclusive_instance():
    if already_running():
        print("ValChange is already running")
        exit(1)
