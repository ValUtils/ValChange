from infi.systray import SysTrayIcon
from os import _exit as quit
from ValImgs import get_imgs

from .exit import fault, lock, unlock, clean_exit
from .config import get_config, get_password
from .launch import launch_valorant, valorant_start
from .structs import ChangeUser


def create_tray(cUser: ChangeUser):
    def on_quit_callback(systray: SysTrayIcon):
        clean_exit(cUser)
        quit(0)
    menu_options = ((f"Current user: {cUser.username}", None, lambda: ""),)
    systray = SysTrayIcon(get_imgs("icon.ico"), "ValChange",
                          menu_options, on_quit=on_quit_callback)
    systray.start()
    return systray


def launch(cUser: ChangeUser):
    if (cUser.isDefault):
        launch_valorant()
        return
    get_password(cUser)
    valorant_start(cUser)


def change(cUser: ChangeUser):
    lock(cUser)

    systray = create_tray(cUser)

    launch(cUser)

    systray.shutdown()
    unlock()


def main():
    fault()
    cUser = get_config()
    change(cUser)
