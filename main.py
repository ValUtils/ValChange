from infi.systray import SysTrayIcon
from os import _exit as quit

from .config import get_config
from .launch import valorant_start

def create_tray(user):
	def on_quit_callback(systray: SysTrayIcon):
		quit(0)
	menu_options = ((f"Current user: {user}", None, lambda: ""),)
	systray = SysTrayIcon("explorer", "ValChange", menu_options, on_quit=on_quit_callback)
	systray.start()
	return systray

def main():
	cUser = get_config()

	if (cUser.isDefault):
		return

	systray = create_tray(cUser.username)

	valorant_start(cUser)

	systray.shutdown()
