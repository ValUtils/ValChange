from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dataclasses_json import DataClassJsonMixin, config

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
    systray: bool
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
class Program(DataClassJsonMixin):
    path: Path = field(metadata=config(decoder=Path))
    beforeLaunch: bool = True
    close: bool = True
    extraExecutables: str = ""
    waitFor: str = ""
    arguments: list[str] = field(default_factory=list)


@dataclass
class Programs(DataClassJsonMixin):
    launcher: Program = field(default=Program(Path("NonExistant")))
    extra: List[Program] = field(default_factory=list)
