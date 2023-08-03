from pathlib import Path

from ..debug import Level, log
from ..proc import wait_process_close, wait_process_open
from ..riot import get_product_info
from .structs import Linker


class InvalidLocaleException(BaseException):
    pass


def linker(og: Path, new: Path):
    log(Level.DEBUG, f"Linking {new} to {og}", "locale")
    og.unlink(missing_ok=True)
    new.link_to(og)
    og_sig = og.with_suffix(".sig")
    og_sig.unlink()
    new.with_suffix(".sig").link_to(og_sig)


def link(locale: str):
    log(Level.DEBUG, f"Started link for {locale}", "locale")
    product = get_product_info()
    l = Linker(locale, product)
    wait_process_open("VALORANT.exe")
    log(Level.DEBUG, f"Valorant launched, linking text", "locale")
    linker(l.pak_path, l.text_locale)
    wait_process_close("VALORANT-Win64-Shipping.exe")
    log(Level.DEBUG, f"Valorant stopped, linking original locale", "locale")
    linker(l.pak_path, l.original_locale)


def unlink():
    product = get_product_info()
    l = Linker("", product)
    log(Level.FULL, "Forcefully linking original locale")
    linker(l.pak_path, l.original_locale)
