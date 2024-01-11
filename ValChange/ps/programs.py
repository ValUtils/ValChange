from typing import List

from ..debug import Level, log
from ..storage import changePath, get_settings
from ..structs import Programs
from .proc import kill_all, wait_process_open
from .subproc import runs


def waits_open(programs: List[str]):
    for p in programs:
        wait_process_open(p)


def get_programs():
    programs = get_settings(Programs, changePath / "programs.json")
    return programs


def pre_launch(programs: Programs):
    log(Level.DEBUG, f"Executing pre-launch programs")
    extra = programs.extra
    launch = [p for p in extra if p.beforeLaunch]
    wait = [p.waitFor for p in extra if p.waitFor]
    runs(launch)
    waits_open(wait)


def post_launch(programs: Programs):
    log(Level.DEBUG, "Executing post-launch programs")
    extra = programs.extra
    launch = [p for p in extra if not p.beforeLaunch]
    runs(launch)


def exit_programs(programs: Programs):
    log(Level.DEBUG, "Killing programs")
    close = [p.path.name for p in programs.extra if p.close]
    extraExecs = [p.extraExecutables for p in programs.extra if p.close]
    kill_all(close)
    kill_all(extraExecs)
