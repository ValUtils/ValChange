import os
import psutil
from time import sleep
from typing import List


def find_procs_by_name(name: str):
    ls: List[psutil.Process] = []
    for p in psutil.process_iter(["exe"]):
        try:
            if os.path.basename(p.exe()) == name:
                ls.append(p)
        except psutil.AccessDenied:
            pass
    return ls


def wait_process_close(name: str):
    ls = find_procs_by_name(name)
    psutil.wait_procs(ls)


def wait_process_open(name: str):
    while True:
        procs = find_procs_by_name(name)
        if (len(procs) > 0):
            return
        sleep(1)


def kill_all(nameList: List[str]):
    ls: List[psutil.Process] = []
    for p in psutil.process_iter(["exe"]):
        try:
            if os.path.basename(p.exe()) in nameList:
                p.kill()
                ls.append(p)
        except psutil.AccessDenied:
            pass
    psutil.wait_procs(ls)
