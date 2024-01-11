from pathlib import Path

from .folders import *
from ..debug import Level, log
from ..ps import subrun, subrun_out
from ..riot import get_product_info
from ..storage import changePath, get_settings, json_write
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
    log(Level.FULL, "Creating output directory", "locale")
    paks = pak_path(path / "output")
    paks.mkdir(parents=True)


def link_before_download(path: Path):
    log(Level.FULL, "Linking old files before downloading", "locale")
    make_output(path)
    paks = pak_path(path / "output")
    link_all(path, paks)


def link_missing_files(path: Path):
    log(Level.FULL, "Linking new files to base directory", "locale")
    paks = pak_path(path / "output")
    link_all(paks, path)


def get_path(manifest: Manifest):
    if manifest.region:
        return lines / manifest.id
    return lines


def remove_unused(locale: str):
    log(Level.DEBUG,
        f"Removing unused paks from Valorant folder for {locale}", "locale")
    paks = pak_path(product.path)
    for f in paks.glob(f"[!{locale}]*?_[Audio|Text]*"):
        f.unlink()


def manage_output(line: str):
    log(Level.FULL, line, "locale")


def manifest_downloader(manifest: Manifest, args: str, path: Path):
    log(Level.FULL,
        f"Downloading manifest {args=} {manifest.region=}", "locale")
    mpath = locale_info.downloader_path
    cargs = f"{manifest.url} --bundles {manifest.bundle}"
    subrun_out(" ".join((mpath, cargs, args)), manage_output, path)


def download_locale(manifest: Manifest, locale: str):
    log(Level.DEBUG, f"Downloading locale files for {locale}", "locale")
    args = f"--languages {locale} --output ./"
    manifest_downloader(manifest, args, product.path)


def download_text(manifest: Manifest, path: Path, lang=""):
    log(Level.DEBUG, f"Downloading text paks {lang}", "locale")
    link_before_download(path)
    args = f"--languages {lang} --filter Text"
    manifest_downloader(manifest, args, path)
    link_missing_files(path)
    rmtree(path / "output")


def clean_panic(id):
    log(Level.FULL, "Cleaning panic state", "locale")
    if id in folder_stems(lines):
        move_all(lines / id, lines)
        locale_info.id = id
    remove_folders(lines)


def panic():
    log(Level.DEBUG, "Startnig panic state", "locale")
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
