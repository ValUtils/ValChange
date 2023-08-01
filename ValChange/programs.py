from typing import List

from .proc import kill_all, wait_process_open
from .storage import changePath, get_settings
from .structs import Programs
from .subproc import runs


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
