from ..structs import ChangeUser
from ..subproc import run_fn
from .links import link
from .paks import download, download_locale, redownload, remove_unused
from .riot import get_manifest, set_locale


def localization(cUser: ChangeUser):
    settings = cUser.settings
    set_locale(settings.voiceLocale)
    manifest = get_manifest(cUser)
    download(manifest)
    download_locale(manifest, settings.voiceLocale)
    redownload(manifest, settings.textLocale)
    remove_unused(settings.voiceLocale)
    run_fn(lambda: link(cUser.settings.textLocale))
