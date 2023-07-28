from typing import List

from .storage import get_settings, changePath
from .structs import Programs, Program
from .subproc import run, run_fn, runs, subrun
from .proc import wait_process_open, kill_all


def waits_open(programs: List[str]):
    for p in programs:
        wait_process_open(p)


def get_programs():
    programs = get_settings(Programs, changePath / "programs.json")
    return programs


def pre_launch(programs: Programs):
    extra = programs.extra
    launch = [p for p in extra if p.beforeLaunch]
    wait = [p.waitFor for p in extra if p.waitFor]
    runs(launch)
    waits_open(wait)


def post_launch(programs: Programs):
    extra = programs.extra
    launch = [p for p in extra if not p.beforeLaunch]
    runs(launch)


def exit_programs(programs: Programs):
    close = [p.path.name for p in programs.extra if p.close]
    extraExecs = [p.extraExecutables for p in programs.extra if p.close]
    kill_all(close)
    kill_all(extraExecs)
