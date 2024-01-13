from os import _exit as quit

from infi.systray import SysTrayIcon

from ValImgs import get_imgs

from .config import get_config, get_password
from .debug import Level, log
from .exit import clean_exit, fault, unlock
from .launch import launch_valorant, valorant_start
from .locale import localization
from .ps import exclusive_instance
from .structs import ChangeUser, Status


def create_tray(cUser: ChangeUser):
    def on_quit_callback(systray: SysTrayIcon):
        clean_exit()
        quit(0)
    menu_options = ((f"Current user: {cUser.username}", None, lambda: ""),)
    systray = SysTrayIcon(get_imgs("icon.ico"), "ValChange",
                          menu_options, on_quit=on_quit_callback)
    return systray


def destroy_tray(systray: SysTrayIcon):
    systray._on_quit = None
    systray.shutdown()


def launch(cUser: ChangeUser):
    if cUser.isDefault:
        localization(cUser)
        launch_valorant(cUser)
        return
    get_password(cUser)
    valorant_start(cUser)


def change(cUser: ChangeUser):
    cUser.status = Status.LOCK

    systray = create_tray(cUser)
    if cUser.systray:
        log(Level.EXTRA, "Starting systray")
        systray.start()

    launch(cUser)

    destroy_tray(systray)
    unlock()


def main():
    exclusive_instance()
    fault()
    cUser = get_config()
    change(cUser)
