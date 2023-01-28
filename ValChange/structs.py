from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from pathlib import Path
from typing import List
from ValLib import User


@dataclass
class Settings(DataClassJsonMixin):
    defaultConfig: str = ""
    defaultUser: str = ""
    pull: bool = False


@dataclass
class ChangeUser():
    user: User
    defaultUser: str
    cfg: str
    pull: bool
    username: str = field(init=False)
    isDefault: bool = field(init=False)

    def __post_init__(self):
        if not self.user:
            return
        self.username = self.user.username
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
