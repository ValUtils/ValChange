from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from pathlib import Path
from typing import List
from ValLib import User


@dataclass
class Settings(DataClassJsonMixin):
    textLocale: str = ""
    voiceLocale: str = ""
    defaultConfig: str = ""
    defaultUser: str = ""
    pull: bool = False


@dataclass
class ChangeUser(DataClassJsonMixin):
    user: User
    settings: Settings
    defaultUser: str = field(init=False)
    cfg: str = field(init=False)
    pull: bool = field(init=False)
    username: str = field(init=False)
    isDefault: bool = field(init=False)

    def __post_init__(self):
        if not self.user:
            return
        self.username = self.user.username
        self.defaultUser = self.settings.defaultUser
        self.cfg = self.settings.defaultConfig
        self.pull = self.settings.pull
        self.isDefault = self.username == self.defaultUser


@dataclass
class Program():
    path: Path
    type: str
    beforeLaunch: bool
    close: bool


@dataclass
class Programs():
    beforeLaunch: List[Program] = field(default_factory=list)
    afterLaunch: List[Program] = field(default_factory=list)
    list: List[Program] = field(default_factory=list)
    launcher: Program = field(init=False)


@dataclass
class Product():
    root: Path
    path: Path
    paks: Path
    locale: str
