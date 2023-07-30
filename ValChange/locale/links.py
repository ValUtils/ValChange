from pathlib import Path

from ..proc import wait_process_close, wait_process_open
from ..riot import get_product_info
from .structs import Linker


class InvalidLocaleException(BaseException):
    pass


def linker(og: Path, new: Path):
    og.unlink()
    new.link_to(og)
    og_sig = og.with_suffix(".sig")
    og_sig.unlink()
    new.with_suffix(".sig").link_to(og_sig)


def link(locale: str):
    product = get_product_info()
    l = Linker(locale, product)
    wait_process_open("VALORANT.exe")
    linker(l.pak_path, l.text_locale)
    wait_process_close("VALORANT-Win64-Shipping.exe")
    linker(l.pak_path, l.original_locale)


def unlink():
    product = get_product_info()
    l = Linker("", product)
    linker(l.pak_path, l.original_locale)
