from argparse import ArgumentParser

from ValVault.terminal import User, get_name, get_pass, init_vault

from .debug import Level, log
from .storage import changePath, get_settings
from .structs import ChangeUser, Settings


def get_args(settings: Settings):
    parser = ArgumentParser("ValChange")
    parser.add_argument("user", help="user to start valorant", nargs="?")
    parser.add_argument("--no-systray", help="don't show a systray",
                        required=False, default=True, action='store_false')
    parser.add_argument("--vanilla", help="launch VALORANT only",
                        required=False, default=False, action='store_true')
    args = parser.parse_args()
    if not args.user:
        return (settings.defaultUser, args.no_systray, args.vanilla)
    init_vault()
    return (get_name(args.user), args.no_systray, args.vanilla)


def get_config(name=""):
    log(Level.DEBUG,
        f"Getting config for {(name if name else 'default user')}")
    settings = get_settings(Settings, changePath / "config.json")
    (username, tray, vanilla) = get_args(settings)
    user = User(name or username, "")
    cUser = ChangeUser(user, settings, tray, vanilla)
    return cUser


def get_password(cUser: ChangeUser):
    log(Level.FULL, f"Getting pasword for {cUser.username}")
    init_vault()
    cUser.user.password = get_pass(cUser.username)
