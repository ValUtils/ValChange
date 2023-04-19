import subprocess
from typing import List
from threading import Thread
from pathlib import Path

from .structs import Program


def run_fn(fn):
    thread = Thread(target=fn)
    thread.start()


def subrun(command: str, cwd=Path.cwd()):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    p = subprocess.Popen(command, cwd=cwd, startupinfo=startupinfo)
    p.wait()


def run(program: Program):
    def subrun():
        path = program.path
        cwd = program.path.parent
        subprocess.run("", executable=path, cwd=cwd)
    thread = Thread(target=subrun)
    thread.start()


def runs(programs: List[Program]):
    for p in programs:
        run(p)
