import subprocess
from typing import List
from threading import Thread

from .structs import Program


def run_fn(fn):
    thread = Thread(target=fn)
    thread.start()


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
