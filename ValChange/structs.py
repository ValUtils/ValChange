from dataclasses import dataclass, field
from enum import IntEnum, auto
from pathlib import Path
from typing import List

from dataclasses_json import DataClassJsonMixin, config

from ValLib import User

from .exit import lock


class Status(IntEnum):
    BOOT = 0
    LOCK = 1
    CONFIG = 2
    COOKIES = 3
    LAUNCHED = 4
    EXITED = 5
    COOKIES_RESTORED = 6
    CLEANED = 7


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
    _status: Status = field(default=Status.BOOT)
    defaultUser: str = field(init=False)
    cfg: str = field(init=False)
    pull: bool = field(init=False)
    username: str = field(init=False)
    isDefault: bool = field(init=False)
    restoreConfig: bool = field(default=False)
    restoreLoadout: bool = field(default=False)

    def __post_init__(self):
        if not self.user:
            return
        self.username = self.user.username
        self.defaultUser = self.settings.defaultUser
        self.cfg = self.settings.defaultConfig
        self.pull = self.settings.pull
        self.isDefault = self.username == self.defaultUser

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, status: Status):
        self._status = status
        lock(self)


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
