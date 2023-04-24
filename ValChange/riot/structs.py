from dataclasses import dataclass
from pathlib import Path


@dataclass
class Product():
    root: Path
    path: Path
    paks: Path
    locale: str
