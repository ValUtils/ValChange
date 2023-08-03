from ..debug import Level, log
from ..structs import ChangeUser
from ..subproc import run_fn
from .links import link
from .paks import download, download_locale, redownload, remove_unused
from .riot import get_manifest, set_locale


def localization(cUser: ChangeUser):
    voice = cUser.settings.voiceLocale
    text = cUser.settings.textLocale
    log(Level.INFO, f"Start localization {voice=} {text=}", "locale")
    set_locale(voice)
    manifest = get_manifest(cUser)
    download(manifest)
    download_locale(manifest, voice)
    redownload(manifest, text)
    remove_unused(voice)
    run_fn(lambda: link(text))
