from pathlib import Path
from shutil import move, rmtree


def get_folders(path: Path):
    return (d for d in path.iterdir() if d.is_dir())


def folder_stems(path: Path):
    return [d.stem for d in get_folders(path)]


def all_files(path: Path):
    return path.glob("*.*")


def move_all(source: Path, target: Path):
    for file in all_files(source):
        move(file, target)


def remove_folders(path: Path):
    for d in get_folders(path):
        rmtree(d)


def link(file: Path, directory: Path):
    try:
        file.link_to(directory / file.name)
    except FileExistsError:
        pass


def link_all(source: Path, target: Path):
    for file in all_files(source):
        link(file, target)


__all__ = [
    "get_folders", "folder_stems",
    "move_all", "link_all",
    "remove_folders", "rmtree"
]
