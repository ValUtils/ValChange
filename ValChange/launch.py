from pathlib import Path
from time import sleep

from .debug import Level, log
from .locale import localization
from .proc import process_exists, wait_process_close, wait_process_open
from .programs import exit_programs, get_programs, post_launch, pre_launch
from .riot import get_riot_installs, restore_options, set_options
from .structs import ChangeUser, Programs
from .subproc import run, run_fn, subrun
from .switch import restore_user, switch_user


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
    log(Level.DEBUG, "Launching Valorant with RiotLauncher")
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
    if programs.launcher.path.exists():
        log(Level.FULL,
            f"Launching Valorant with {programs.launcher.path.stem}")
        run(programs.launcher)
        return
    run_fn(riot_launcher)


def launch_valorant():
    programs = get_programs()
    pre_launch(programs)
    valorant_launcher(programs)
    client_hack()
    wait_process_open("VALORANT-Win64-Shipping.exe")
    post_launch(programs)
    wait_process_close("VALORANT.exe")
    exit_programs(programs)
