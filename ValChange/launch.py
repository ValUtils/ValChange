from pathlib import Path
from time import sleep

from .debug import Level, log
from .locale import localization
from .ps import (
    exit_programs,
    get_programs,
    post_launch,
    pre_launch,
    process_exists,
    run,
    run_fn,
    subrun,
    wait_process_close,
    wait_process_open
)
from .riot import get_riot_installs, restore_options, set_options
from .structs import ChangeUser, Programs, Status
from .switch import restore_user, switch_user


def valorant_start(cUser: ChangeUser):
    set_options(cUser)

    switch_user(cUser)

    localization(cUser)

    launch_valorant(cUser)
    wait_process_open("VALORANT.exe")
    cUser.status = Status.LAUNCHED
    wait_process_close("VALORANT.exe")
    cUser.status = Status.EXITED

    restore_user()
    cUser.status = Status.COOKIES_RESTORED

    restore_options(cUser)
    cUser.status = Status.CLEANED


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


def launch_all():
    programs = get_programs()
    pre_launch(programs)
    valorant_launcher(programs)
    client_hack()
    wait_process_open("VALORANT-Win64-Shipping.exe")
    post_launch(programs)
    wait_process_close("VALORANT.exe")
    exit_programs(programs)


def launch_valorant(cUser: ChangeUser):
    if cUser.vanilla:
        riot_launcher()
        return
    run_fn(launch_all)
