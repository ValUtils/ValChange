from ValLib.api import get_region
from ValLib import authenticate

from ..structs import ChangeUser
from ..product import product_path
from ..storage import read_yaml, write_yaml

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
        auth = authenticate(cUser.user)
        region = get_region(auth)
        return get_region_manifest(region)
