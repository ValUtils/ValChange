
from pathlib import Path
from urllib.parse import urlparse as URL

import requests

from ..debug import Level, log
from .structs import Manifest


class UnkownRegionException(BaseException):
    pass


class PatchDifferenceException(BaseException):
    pass


def get_region_configs():
    log(Level.FULL, "Getting manifest region configs", "locale")
    host = "https://clientconfig.rpg.riotgames.com"
    end_point = "/api/v1/config/public"
    args = {
        "namespace": "keystone.products.valorant.patchlines"
    }
    r = requests.get(host + end_point, params=args)

    patch = "keystone.products.valorant.patchlines.live"
    v = r.json()[patch]["platforms"]["win"]
    return v["configurations"]


def get_region_manifest(region: str):
    log(Level.DEBUG, f"Getting manifest for {region}", "locale")
    configs = get_region_configs()
    items = [c for c in configs if c["id"] == region]
    if not items:
        raise UnkownRegionException
    cfg = items[0]
    url = cfg["patch_url"]
    manifest_id = get_manifest_id(cfg["patch_url"])
    bundle = cfg["bundles_url"]
    return Manifest(url, manifest_id, bundle, True)


def get_manifest_id(manifest_url: str):
    url_path = URL(manifest_url).path
    path = Path(url_path)
    id = path.stem
    log(Level.VERBOSE, f"Manifest {id=}")
    return id


def get_seamless_manifest():
    log(Level.DEBUG, f"Getting seamless manifest", "locale")
    configs = get_region_configs()
    patches = [c["patch_url"] for c in configs]
    if not len(set(patches)) == 1:
        raise PatchDifferenceException

    url = patches[0]
    manifest_id = get_manifest_id(patches[0])
    bundle = configs[0]["bundles_url"]

    return Manifest(url, manifest_id, bundle)


__all__ = [
    "get_seamless_manifest", "get_region_manifest",
    "PatchDifferenceException"
]
