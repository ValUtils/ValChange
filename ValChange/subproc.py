import subprocess
from pathlib import Path
from threading import Thread
from typing import List

from .structs import Program

pool: List[Thread] = []


def run_fn(fn):
    thread = Thread(target=fn)
    pool.append(thread)
    thread.start()


def wait_threads():
    for t in pool:
        t.join()


def subrun(command: str, cwd=Path.cwd()):
    log(Level.VERBOSE, f"Running without window {command}")
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    p = subprocess.Popen(command, cwd=cwd, startupinfo=startupinfo)
    p.wait()


def run(program: Program):
    log(Level.VERBOSE, f"Running {program.path.stem}")

    def subrun():
        path = program.path
        cwd = program.path.parent
        subprocess.run(args=program.arguments, executable=path, cwd=cwd)
    thread = Thread(target=subrun)
    thread.start()


def runs(programs: List[Program]):
    for p in programs:
        run(p)
