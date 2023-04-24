from os import getenv
from pathlib import Path

from ..storage import read_yaml, json_read

from .structs import Product

ProgramData = getenv("ProgramData", "")
riot_data = Path(ProgramData) / "Riot Games"
meta_valorant = riot_data / "Metadata" / "valorant.live"
product_path = meta_valorant / "valorant.live.product_settings.yaml"


def get_product_info():
    product = read_yaml(product_path)
    root = Path(product["product_install_root"])
    path = Path(product["product_install_full_path"])
    paks = path / "ShooterGame" / "Content" / "Paks"
    return Product(
        root,
        path,
        paks,
        product["settings"]["locale"]
    )


def get_riot_installs():
    riotInstallsPath = riot_data / "RiotClientInstalls.json"
    return json_read(riotInstallsPath)
