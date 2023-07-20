from pathlib import Path
from time import sleep

from .subproc import run, run_fn, runs, subrun
from .structs import ChangeUser, Program, Programs
from .switch import switch_user, restore_user
from .proc import kill_all, wait_process_close, wait_process_open, process_exists
from .riot import get_riot_installs, set_options, restore_options
from .locale import localization
from .storage import json_read, changePath


def valorant_start(cUser: ChangeUser):
    set_options(cUser)

    switch_user(cUser.user)

    localization(cUser)

    run_fn(launch_valorant)
    wait_process_open("VALORANT.exe")
    wait_process_close("VALORANT.exe")

    restore_user()

    restore_options(cUser)


def get_programs():
    programsData = json_read(changePath / "programs.json")
    programs = Programs()
    for p in programsData:
        program = Program.from_dict(p)
        programs.list.append(program)
        if program.type == "launcher":
            programs.launcher = program
        elif program.beforeLaunch:
            programs.beforeLaunch.append(program)
        else:
            programs.afterLaunch.append(program)
    return programs


def riot_launcher():
    installs = get_riot_installs()
    client_path = Path(installs["rc_default"])
    args = "--launch-product=valorant --launch-patchline=live"
    subrun(f'"{client_path}" {args}')


def client_hack():
    while True:
        if process_exists("VALORANT.exe"):
            return
        if process_exists("RiotClientUx.exe"):
            break
        sleep(1)
    sleep(1)
    run_fn(riot_launcher)


def valorant_launcher(programs: Programs):
    if programs.launcher:
        run(programs.launcher)
        return
    run_fn(riot_launcher)


def launch_valorant():
    programs = get_programs()
    runs(programs.beforeLaunch)
    [wait_process_open(p.waitFor) for p in programs.list if p.waitFor]
    valorant_launcher(programs)
    client_hack()
    wait_process_open("VALORANT.exe")
    runs(programs.afterLaunch)
    wait_process_close("VALORANT.exe")
    kill_all([p.path.name for p in programs.list if p.close])
    kill_all([p.extraExecutables for p in programs.list if p.close])
