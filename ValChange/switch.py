from ValLib import User

from .proc import kill_all
from .riot import get_auth, get_cookies, save_cookies
from .storage import changePath, json_read, json_write

images = [
    "LeagueClient.exe",
    "LoR.exe",
    "VALORANT.exe",
    "VALORANT-Win64-Shipping.exe",
    "RiotClientServices.exe",
    "RiotClientUx.exe",
    "RiotClientUxRender.exe"
]

switched = False


def store_cookies():
    json_write(get_cookies(), changePath / "cookies.json")
    global switched
    switched = True


def restore_cookies():
    if not switched:
        return
    save_cookies(json_read(changePath / "cookies.json"))


def switch_user(user: User):
    store_cookies()

    cookies = get_auth(user).cookies
    kill_all(images)
    save_cookies(cookies)


def restore_user():
    kill_all(images)
    restore_cookies()
