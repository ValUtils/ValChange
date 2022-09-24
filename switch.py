from ValVault import User
from ValConfig.storage import jsonRead, jsonWrite, settingsPath

from .proc import kill_all
from .cookies import get_cookies, save_cookies
from .auths import clientAuth

images = [
	"LeagueClient.exe",
	"LoR.exe",
	"VALORANT.exe",
	"VALORANT-Win64-Shipping.exe",
	"RiotClientServices.exe",
	"RiotClientUx.exe",
	"RiotClientUxRender.exe"
]

def store_cookies():
	jsonWrite(get_cookies(), settingsPath / "switcher" / "cookies.json")

def restore_cookies():
	save_cookies(jsonRead(settingsPath / "switcher" / "cookies.json"))

def switch_user(user: User):
	store_cookies()

	cookies = clientAuth(user)
	kill_all(images)
	save_cookies(cookies)

def restore_user():
	kill_all(images)
	restore_cookies()