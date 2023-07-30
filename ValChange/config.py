from argparse import ArgumentParser
from ValVault.terminal import get_pass, get_name, init_vault, User

from .structs import ChangeUser, Settings
from .storage import get_settings, changePath


def get_args(settings: Settings):
    parser = ArgumentParser("ValChange")
    parser.add_argument("user", help="user to start valorant", nargs="?")
    parser.add_argument("--no-systray", help="don't show a systray",
                        required=False, default=True, action='store_false')
    args = parser.parse_args()
    if not args.user:
        return (settings.defaultUser, args.no_systray)
    init_vault()
    return (get_name(args.user), args.no_systray)


def get_config(name=""):
    settings = get_settings(Settings, changePath / "config.json")
    (username, tray) = get_args(settings)
    user = User(name or username, "")
    cUser = ChangeUser(user, settings, tray)
    return cUser


def get_password(cUser: ChangeUser):
    init_vault()
    cUser.user.password = get_pass(cUser.username)
