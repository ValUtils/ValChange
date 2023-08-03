from pathlib import Path
from shutil import move, rmtree

from ..debug import Level, log


def get_folders(path: Path):
    return (d for d in path.iterdir() if d.is_dir())


def folder_stems(path: Path):
    return [d.stem for d in get_folders(path)]


def all_files(path: Path):
    return path.glob("*.*")


def move_all(source: Path, target: Path):
    log(Level.FULL, f"Moving {source} files to {target}", "locale")
    for file in all_files(source):
        move(file, target)


def remove_folders(path: Path):
    log(Level.FULL, f"Removing folders in {path}", "locale")
    for d in get_folders(path):
        rmtree(d)


def link(file: Path, directory: Path):
    try:
        file.link_to(directory / file.name)
    except FileExistsError:
        log(Level.VERBOSE, f"Can't link {file.name} to {directory}", "locale")
        pass


def link_all(source: Path, target: Path):
    log(Level.FULL, f"Linking all files from {source} to {target}", "locale")
    for file in all_files(source):
        link(file, target)


__all__ = [
    "get_folders", "folder_stems",
    "move_all", "link_all",
    "remove_folders", "rmtree"
]
