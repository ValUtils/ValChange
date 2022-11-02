from infi.systray import SysTrayIcon
from os import _exit as quit

from .exit import fault, lock, unlock, clean_exit
from .config import get_config, get_password
from .launch import launch_valorant, valorant_start

def create_tray(user):
	def on_quit_callback(systray: SysTrayIcon):
		clean_exit()
		quit(0)
	menu_options = ((f"Current user: {user}", None, lambda: ""),)
	systray = SysTrayIcon("explorer", "ValChange", menu_options, on_quit=on_quit_callback)
	systray.start()
	return systray

def main():
	fault()

	cUser = get_config()

	lock(cUser)

	if (cUser.isDefault):
		launch_valorant()
		return

	systray = create_tray(cUser.username)

	get_password(cUser)
	valorant_start(cUser)

	systray.shutdown()
	unlock()
