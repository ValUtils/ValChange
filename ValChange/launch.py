from pathlib import Path
from time import sleep

from .subproc import run, run_fn, subrun
from .structs import ChangeUser, Programs
from .switch import switch_user, restore_user
from .proc import wait_process_close, wait_process_open, process_exists
from .riot import get_riot_installs, set_options, restore_options
from .programs import get_programs, pre_launch, post_launch, exit_programs
from .locale import localization


def valorant_start(cUser: ChangeUser):
    set_options(cUser)

    switch_user(cUser.user)

    localization(cUser)

    run_fn(launch_valorant)
    wait_process_open("VALORANT.exe")
    wait_process_close("VALORANT.exe")

    restore_user()

    restore_options(cUser)


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
    pre_launch(programs)
    valorant_launcher(programs)
    client_hack()
    wait_process_open("VALORANT.exe")
    post_launch(programs)
    wait_process_close("VALORANT.exe")
    exit_programs(programs)
