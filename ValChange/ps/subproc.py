import subprocess
from pathlib import Path
from threading import Thread
from typing import Callable, List

from ..debug import Level, log
from ..structs import Program

pool: List[Thread] = []


def run_fn(fn):
    thread = Thread(target=fn)
    pool.append(thread)
    thread.start()


def wait_threads():
    for t in pool:
        t.join()


def startup_info():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return startupinfo


def subrun_out(command: str, output: Callable[[str], None], cwd=Path.cwd()):
    p = subprocess.Popen(
        command,
        cwd=cwd,
        text=True,
        startupinfo=startup_info(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    if p.stdout is None:
        p.wait()
        return

    for line in iter(p.stdout.readline, ''):
        output(line.strip())

    p.wait()


def subrun(command: str, cwd=Path.cwd()):
    log(Level.VERBOSE, f"Running without window {command}")
    p = subprocess.Popen(command, cwd=cwd, startupinfo=startup_info())
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
