
from infi.systray import SysTrayIcon
from switch import switch_user, restore_user
from proc import wait_process_close, wait_process_open
from os import _exit

from .structs import ChangeUser
from .options import set_options, restore_options
from .config import get_config

def create_tray(user):
	def on_quit_callback(systray: SysTrayIcon):
		_exit(0)
	menu_options = ((f"Current user: {user}", None, lambda: ""),)
	systray = SysTrayIcon("explorer", "ValChange", menu_options, on_quit=on_quit_callback)
	systray.start()
	return systray

def valorant_start(cUser: ChangeUser):
	set_options(cUser)

	switch_user(cUser.user)

	wait_process_open("VALORANT.exe")
	wait_process_close("VALORANT.exe")

	restore_user()

	restore_options(cUser)

def main():
	cUser = get_config()

	if (cUser.isDefault):
		return

	systray = create_tray(cUser.username)

	valorant_start(cUser)

	systray.shutdown()
