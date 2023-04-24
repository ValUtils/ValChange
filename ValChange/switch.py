from ValLib import User

from .proc import kill_all
from .cookies import get_cookies, save_cookies
from .auths import client_auth
from .storage import json_read, json_write, changePath

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
    json_write(get_cookies(), changePath / "cookies.json")


def restore_cookies():
    save_cookies(json_read(changePath / "cookies.json"))


def switch_user(user: User):
    store_cookies()

    cookies = client_auth(user)
    kill_all(images)
    save_cookies(cookies)


def restore_user():
    kill_all(images)
    restore_cookies()
