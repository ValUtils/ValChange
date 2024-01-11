from .debug import Level, log
from .ps import kill_all
from .riot import get_auth, get_cookies, save_cookies
from .storage import changePath, json_read, json_write
from .structs import ChangeUser, Status

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


def switch_user(cUser: ChangeUser):
    log(Level.DEBUG, f"Switching to {cUser.username}")
    store_cookies()

    cUser.status = Status.COOKIES

    cookies = get_auth(cUser.user).cookies
    kill_all(images)
    save_cookies(cookies)


def restore_user():
    log(Level.DEBUG, "Restoring user cookies")
    kill_all(images)
    restore_cookies()
