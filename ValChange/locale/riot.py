from .manifest import *
from ..config import get_password
from ..debug import Level, log
from ..riot import get_extra_auth, product_path
from ..storage import read_yaml, write_yaml
from ..structs import ChangeUser


class InvalidLocaleException(BaseException):
    pass


def set_locale(locale: str):
    log(Level.VERBOSE, f"Setting locale in product.yml to {locale}", "locale")
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
