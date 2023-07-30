from dataclasses import dataclass, field
from pathlib import Path

from dataclasses_json import DataClassJsonMixin

from ..riot import Product


@dataclass
class Manifest():
    url: str
    id: str
    bundle: str
    region: bool = False


@dataclass
class LocaleInfo(DataClassJsonMixin):
    id: str = ""
    panic: bool = False
    downloader_path: str = ""


@dataclass
class Linker():
    locale: str
    product: Product
    pak_path: Path = field(init=False)
    lines: Path = field(init=False)
    original_locale: Path = field(init=False)
    text_locale: Path = field(init=False)

    def _text(self, locale: str):
        return locale + "_Text-WindowsClient.pak"

    def __post_init__(self):
        self.lines = self.product.root / "TextPaks"
        self.pak_path = self.product.paks / self._text(self.product.locale)
        self.original_locale = self.lines / self._text(self.product.locale)
        self.text_locale = self.lines / self._text(self.locale)
