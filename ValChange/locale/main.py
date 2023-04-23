from ..subproc import run_fn
from ..structs import ChangeUser

from .links import link
from .riot import set_locale, get_manifest
from .paks import download_locale, download, redownload, remove_unused


def localization(cUser: ChangeUser):
    settings = cUser.settings
    set_locale(settings.voiceLocale)
    manifest = get_manifest(cUser)
    download(manifest)
    download_locale(manifest, settings.voiceLocale)
    redownload(manifest, settings.textLocale)
    remove_unused(settings.voiceLocale)
    run_fn(lambda: link(cUser.settings.textLocale))
