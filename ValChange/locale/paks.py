from pathlib import Path

from ..subproc import subrun
from ..product import get_product_info
from ..storage import get_settings, json_write, changePath

from .folders import *
from .structs import LocaleInfo, Manifest

locale_path = changePath / "locale.json"
locale_info = get_settings(LocaleInfo, locale_path)
product = get_product_info()
lines = product.root / "TextPaks"

lines.mkdir(exist_ok=True)


def save_settings():
    json_write(locale_info.to_dict(), locale_path)


def pak_path(path: Path):
    return path / "ShooterGame" / "Content" / "Paks"


def make_output(path: Path):
    paks = pak_path(path / "output")
    paks.mkdir(parents=True)


def link_before_download(path: Path):
    make_output(path)
    paks = pak_path(path / "output")
    link_all(path, paks)


def link_missing_files(path: Path):
    paks = pak_path(path / "output")
    link_all(paks, path)


def get_path(manifest: Manifest):
    if manifest.region:
        return lines / manifest.id
    return lines


def remove_unused(locale: str):
    paks = pak_path(product.path)
    for f in paks.glob(f"[!{locale}]*?_[Audio|Text]*"):
        f.unlink()


def manifest_downloader(manifest: Manifest, args: str, path: Path):
    mpath = locale_info.downloader_path
    cargs = f"{manifest.url} --bundles {manifest.bundle}"
    subrun(" ".join((mpath, cargs, args)), path)


def download_locale(manifest: Manifest, locale: str):
    args = f"--languages {locale} --output ./"
    manifest_downloader(manifest, args, product.path)


def download_text(manifest: Manifest, path: Path, lang=""):
    link_before_download(path)
    args = f"--languages {lang} --filter Text"
    manifest_downloader(manifest, args, path)
    link_missing_files(path)
    rmtree(path / "output")


def clean_panic(id):
    if id in folder_stems(lines):
        move_all(lines / id, lines)
        locale_info.id = id
    remove_folders(lines)


def panic():
    locale_info.panic = True
    target = lines / locale_info.id
    target.mkdir(exist_ok=True)
    move_all(lines, target)


def handle_panic(manifest: Manifest):
    if manifest.region:
        panic()
        return

    if not locale_info.panic:
        clean_panic(manifest.id)
        return


def redownload(manifest: Manifest, locale: str):
    path = get_path(manifest)
    download_text(manifest, path, locale)


def download(manifest: Manifest):
    if manifest.id == locale_info.id:
        return
    handle_panic(manifest)
    path = get_path(manifest)
    download_text(manifest, path)
    locale_info.id = manifest.id
    save_settings()
