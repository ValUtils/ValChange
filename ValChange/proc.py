import os
from time import sleep
import psutil


def find_procs_by_name(name):
    ls = []
    for p in psutil.process_iter(["exe"]):
        try:
            if os.path.basename(p.exe()) == name:
                ls.append(p)
        except psutil.AccessDenied:
            pass
    return ls


def wait_process_close(name):
    ls = find_procs_by_name(name)
    psutil.wait_procs(ls)


def wait_process_open(name: str):
    while True:
        procs = find_procs_by_name(name)
        if (len(procs) > 0):
            return
        sleep(1)


def kill_all(nameList):
    ls = []
    for p in psutil.process_iter(["exe"]):
        try:
            if os.path.basename(p.exe()) in nameList:
                p.kill()
                ls.append(p)
        except psutil.AccessDenied:
            pass
    psutil.wait_procs(ls)
