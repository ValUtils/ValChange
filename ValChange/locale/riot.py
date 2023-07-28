from ..structs import ChangeUser
from ..riot import product_path
from ..config import get_password
from ..storage import read_yaml, write_yaml
from ..helper import get_extra_auth

from .manifest import *


class InvalidLocaleException(BaseException):
    pass


def set_locale(locale: str):
    product = read_yaml(product_path)
    available_locales = product["locale_data"]["available_locales"]
    if locale not in available_locales:
        raise InvalidLocaleException
    product["settings"]["locale"] = locale
    write_yaml(product_path, product)


def get_manifest(cUser: ChangeUser):
    try:
        return get_seamless_manifest()
    except PatchDifferenceException:
        if cUser.defaultUser:
            get_password(cUser)
        auth = get_extra_auth(cUser.user)
        return get_region_manifest(auth.region)
